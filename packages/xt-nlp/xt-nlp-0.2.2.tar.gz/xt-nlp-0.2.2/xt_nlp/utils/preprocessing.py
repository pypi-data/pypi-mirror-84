import os
import collections
import pickle
import random 

from .ses_utils import SESFeature, SESAnswer, SESExample
from .statistics import print_example_stats, print_feature_stats

import logging

def split_examples(examples, train_prop, seed=None):
    """Splits up examples into a train and val set of examples

    Args:
        examples (list{SESExamples}): List of SESExamples to split. Each example corresponds to 1 document
        train_prop (float): Proportion of examples in the training set
        seed (int, optional): Random seed. Defaults to None.

    Returns:
        tuple(list{SESExamples}, list{SESExamples}): Tuple of train and validation examples
    """
    random.seed(seed)
    random.shuffle(examples)
    num_train = int(len(examples)*train_prop)
    train_examples = examples[:num_train]
    val_examples = examples[num_train:]

    return train_examples, val_examples


def get_features(
    examples, 
    tokenizer, 
    all_ans_types,
    max_seq_len=384,
    doc_stride=120,
    cached_feature_dir='.cache/',
    use_cache_features=False,
    mode="train"
):
    """Either gets features from the cache or generates them from a list of examples.
    Each example corresponds to a full document. One document/example can have many features.
    This is based on max_seq_len and doc_stride.

    Args:
        examples (list{SESExample}): List of SESExamples to convert to SESFeatures
        tokenizer (Tokenizer): The tokenizer
        all_ans_types ([type]): All labels that we want to include
        max_seq_len (int, optional): Maximum sequence length of a feature. Defaults to 384.
        doc_stride (int, optional): Length of stride between features. Defaults to 120.
        cached_feature_dir (str, optional): Directory to store the cached features. Defaults to '.cache/'.
        use_cache_features (bool, optional): Load features from cache if it exists. Defaults to False.
        mode (str, optional): Mode. Can be 'train', 'val', or 'test'. Defaults to "train".

    Returns:
        list{XTFeature}: The list of the created XTFeatures
    """

    assert mode in [
        "train",
        "val",
        "test",
    ], f"get_features mode can only be train, val or test. Got {mode}."

    labels_str = "_".join([ans[:4] for ans in all_ans_types])
    feature_dir = f"{mode}_seq{max_seq_len}_doc{doc_stride}_nex{len(examples)}_labs{labels_str}"
    cached_dir = os.path.join(cached_feature_dir, feature_dir)
    cached_features_file = os.path.join(cached_dir, "features.pkl")

    if use_cache_features:
        try:
            with open(cached_features_file, "rb") as reader:
                features = pickle.load(reader)
            assert features is not None

            return features

        except Exception:
            logging.info("Cached Features Not Found. Creating them...")

    features = convert_examples_to_features(
        examples=examples, 
        tokenizer=tokenizer, 
        has_labels=(mode != "test"), 
        all_ans_types=all_ans_types,
        max_seq_len=max_seq_len,
        doc_stride=doc_stride
    )

    # Cache features
    if use_cache_features:
        os.makedirs(cached_dir, exist_ok=True)
        with open(cached_features_file, "wb") as writer:
            pickle.dump(features, writer)

    return features


def convert_examples_to_features(
    examples, 
    tokenizer, 
    has_labels, 
    all_ans_types, 
    max_seq_len, 
    doc_stride
):
    """Converts a list of XTExamples into XTFeatures. Note that one XTExample can have many XTFeatures 

    Args:
        examples (list{XTExample}): The list of XTExamples to be converted into features
        tokenizer (Tokenizer): The tokenizer being used to tokenize the text
        has_labels (bool): Whether or not the examples have annotations/labels
        all_ans_types (list{str}): The list of answer types or classes
        max_seq_len (int): Maximum sequence length for a single feature
        doc_stride (int): Stride length between features.
    """

    def _check_is_max_context(doc_spans, cur_span_index, position):
        """Check if this is the 'max context' doc span for the token."""

        # Because of the sliding window approach taken to scoring documents, a single
        # token can appear in multiple documents. E.g.
        #  Doc: the man went to the store and bought a gallon of milk
        #  Span A: the man went to the
        #  Span B: to the store and bought
        #  Span C: and bought a gallon of
        #  ...
        #
        # Now the word 'bought' will have two scores from spans B and C. We only
        # want to consider the score with "maximum context", which we define as
        # the *minimum* of its left and right context (the *sum* of left and
        # right context will always be the same, of course).
        #
        # In the example the maximum context for 'bought' would be span C since
        # it has 1 left context and 3 right context, while span B has 4 left context
        # and 0 right context.
        best_score = None
        best_span_index = None
        for (span_index, doc_span) in enumerate(doc_spans):
            end = doc_span.start + doc_span.length - 1
            if position < doc_span.start:
                continue
            if position > end:
                continue
            num_left_context = position - doc_span.start
            num_right_context = end - position
            score = min(num_left_context, num_right_context) + 0.01 * doc_span.length
            if best_score is None or score > best_score:
                best_score = score
                best_span_index = span_index

        return cur_span_index == best_span_index

    def _get_all_ans_types(examples):
        """Returns all possible answer types for a list of examples."""
        all_ans_types = []
        for e in examples:
            for a in e.ans_list:
                if a.ans_type not in all_ans_types:
                    all_ans_types.append(a.ans_type)
        return all_ans_types

    def _improve_answer_span(
        doc_tokens, input_start, input_end, tokenizer, orig_answer_text
    ):
        """Returns tokenized answer spans that better match the annotated answer."""

        # The SQuAD annotations are character based. We first project them to
        # whitespace-tokenized words. But then after WordPiece tokenization, we can
        # often find a "better match". For example:
        #
        #   Question: What year was John Smith born?
        #   Context: The leader was John Smith (1895-1943).
        #   Answer: 1895
        #
        # The original whitespace-tokenized answer will be "(1895-1943).". However
        # after tokenization, our tokens will be "( 1895 - 1943 ) .". So we can match
        # the exact answer, 1895.
        #
        # However, this is not always possible. Consider the following:
        #
        #   Question: What country is the top exporter of electornics?
        #   Context: The Japanese electronics industry is the lagest in the world.
        #   Answer: Japan
        #
        # In this case, the annotator chose "Japan" as a character sub-span of
        # the word "Japanese". Since our WordPiece tokenizer does not split
        # "Japanese", we just use "Japanese" as the annotation. This is fairly rare
        # in SQuAD, but does happen.

        tok_answer_text = " ".join(tokenizer.tokenize(orig_answer_text))
        # # logging.info(tok_answer_text)
        for new_start in range(input_start, input_end + 1):
            for new_end in range(input_end, new_start - 1, -1):
                text_span = " ".join(doc_tokens[new_start : (new_end + 1)])
                if text_span == tok_answer_text:
                    return (
                        new_start,
                        new_end,
                    )  # Note: Even though doc_tokens[new_start:new_end+1] is the full answer,
                    # It is the new_end indexed token that is the end token. This is why there is no +1

        # Couldnt find a match. This means the character level annotation was not even indexed with wordpiece
        # For example: MenA --> ['men', '#ac', '##wy', '-', 't']. In this rare case, just use the whole word as label.
        return (input_start, input_end)

    unique_id = 1000000000
    features = []
    
    for (example_index, example) in enumerate(examples):
        tok_to_orig_index = []
        orig_to_tok_index = []
        all_doc_tokens = []
        # two step document tokenization

        # makes doc_tokens
        doc_tokens = []
        char_to_word_offset = []
        prev_is_whitespace = True

        for c in example.text:
            if c.isspace():
                prev_is_whitespace = True
            else:
                if prev_is_whitespace:
                    doc_tokens.append(c)
                else:
                    doc_tokens[-1] += c
                prev_is_whitespace = False
            char_to_word_offset.append(len(doc_tokens) - 1)
        # check for impossibility and make answers
        is_impossible = []
        start_positions = []
        end_positions = []
        orig_answer_texts = []

        if has_labels:
            for (ans_type_i, ans_type) in enumerate(all_ans_types):
                filtered_ans = list(
                    filter(lambda x: x.ans_type == ans_type, example.ans_list)
                )
                start_positions.append(
                    []
                )  # Initialize empty arrays for this ans_type
                end_positions.append([])
                orig_answer_texts.append([])

                if (
                    len(filtered_ans) == 0
                ):  # No answers in this document for this field
                    is_impossible.append(True)
                    start_positions[ans_type_i].append(-1)
                    end_positions[ans_type_i].append(-1)
                    orig_answer_texts[ans_type_i].append("")
                else:
                    for ans in filtered_ans:
                        orig_answer_text = ans.text
                        answer_offset = ans.start_char
                        answer_length = len(orig_answer_text)
                        start_position = char_to_word_offset[answer_offset]
                        end_position = char_to_word_offset[
                            answer_offset + answer_length - 1
                        ]

                        start_positions[ans_type_i].append(start_position)
                        end_positions[ans_type_i].append(end_position)
                        orig_answer_texts[ans_type_i].append(orig_answer_text)
                    is_impossible.append(False)

        # per example
        # splits doc tokens further into sub_tokens
        for (i, token) in enumerate(doc_tokens):
            orig_to_tok_index.append(len(all_doc_tokens))
            sub_tokens = tokenizer.tokenize(token)
            for sub_token in sub_tokens:
                tok_to_orig_index.append(i)
                all_doc_tokens.append(sub_token)
        tok_start_positions = []
        tok_end_positions = []

        if has_labels:
            for (ans_type_i, ans_type) in enumerate(all_ans_types):
                tok_start_positions.append([])
                tok_end_positions.append([])
                if is_impossible[ans_type_i]:
                    tok_start_positions[ans_type_i].append(-1)
                    tok_end_positions[ans_type_i].append(-1)
                if not is_impossible[ans_type_i]:
                    for start_position, end_position, orig_answer_text in zip(
                        start_positions[ans_type_i],
                        end_positions[ans_type_i],
                        orig_answer_texts[ans_type_i],
                    ):
                        tok_start_position = orig_to_tok_index[start_position]
                        if (
                            end_position < len(doc_tokens) - 1
                        ):  # If not the last WS token
                            tok_end_position = (
                                orig_to_tok_index[end_position + 1] - 1
                            )
                        else:
                            tok_end_position = len(all_doc_tokens) - 1
                        # Now we have start and end position within all_doc_tokens
                        tok_start_position, tok_end_position = _improve_answer_span(
                            all_doc_tokens,
                            tok_start_position,
                            tok_end_position,
                            tokenizer,
                            orig_answer_text,
                        )
                        tok_start_positions[ans_type_i].append(tok_start_position)
                        tok_end_positions[ans_type_i].append(tok_end_position)

        # The -2 accounts for [CLS] and [SEP]
        max_tokens_for_doc = max_seq_len - 2

        # We can have documents that are longer than the maximum sequence length.
        # To deal with this we do a sliding window approach, where we take chunks
        # of the up to our max length with a stride of `doc_stride`.
        _DocSpan = collections.namedtuple(  # pylint: disable=invalid-name
            "DocSpan", ["start", "length"]
        )
        doc_spans = []
        start_offset = 0
        while start_offset < len(all_doc_tokens):
            length = len(all_doc_tokens) - start_offset
            if length > max_tokens_for_doc:
                length = max_tokens_for_doc
            doc_spans.append(_DocSpan(start=start_offset, length=length))
            if start_offset + length == len(all_doc_tokens):
                break
            start_offset += min(
                length, doc_stride
            )  # doc_stride should always be lower than length

        for (doc_span_index, doc_span) in enumerate(doc_spans):
            tokens = []
            token_to_orig_map = {}
            token_is_max_context = {}
            segment_ids = []

            # Convert all tokens in this doc_span to input_ids
            tokens.append("[CLS]")
            segment_ids.append(0)
            for i in range(doc_span.length):
                split_token_index = doc_span.start + i
                token_to_orig_map[len(tokens)] = tok_to_orig_index[
                    split_token_index
                ]
                is_max_context = _check_is_max_context(
                    doc_spans, doc_span_index, split_token_index
                )
                token_is_max_context[len(tokens)] = is_max_context
                tokens.append(all_doc_tokens[split_token_index])
                segment_ids.append(1)
            tokens.append("[SEP]")
            segment_ids.append(1)

            input_ids = tokenizer.convert_tokens_to_ids(tokens)

            # The mask has 1 for real tokens and 0 for padding tokens. Only real
            # tokens are attended to.
            input_mask = [1] * len(input_ids)

            # Zero-pad up to the sequence length.
            while len(input_ids) < max_seq_len:
                input_ids.append(0)
                input_mask.append(0)
                segment_ids.append(0)

            assert len(input_ids) == max_seq_len
            assert len(input_mask) == max_seq_len
            assert len(segment_ids) == max_seq_len

            final_start_positions = []
            final_end_positions = []

            if has_labels:
                for (ans_type_i, ans_type) in enumerate(all_ans_types):
                    final_start_positions.append([])
                    final_end_positions.append([])
                    if is_impossible[ans_type_i]:
                        final_start_positions[ans_type_i].append(0)
                        final_end_positions[ans_type_i].append(0)
                    elif not is_impossible[ans_type_i]:
                        for tok_start_position, tok_end_position in zip(
                            tok_start_positions[ans_type_i],
                            tok_end_positions[ans_type_i],
                        ):
                            # For training, if our document chunk does not contain an annotation
                            # we throw it out, since there is nothing to predict.
                            doc_start = doc_span.start
                            doc_end = doc_span.start + doc_span.length - 1
                            # if in span
                            within_span = (
                                tok_start_position >= doc_start
                                and tok_end_position <= doc_end
                            )
                            if within_span:
                                doc_offset = 1  # modifed from len(query_tokens) + 2
                                start_position = (
                                    tok_start_position - doc_start + doc_offset
                                )  # To account for [CLS]?
                                end_position = (
                                    tok_end_position - doc_start + doc_offset
                                )
                                final_start_positions[ans_type_i].append(
                                    start_position
                                )
                                final_end_positions[ans_type_i].append(end_position)
                        if (
                            len(final_start_positions[ans_type_i]) == 0
                            and len(final_end_positions[ans_type_i]) == 0
                        ):
                            # No answers in this span
                            final_start_positions[ans_type_i].append(0)
                            final_end_positions[ans_type_i].append(0)
                            # is_impossible[ans_type_i] = True
                            
            features.append(
                SESFeature(
                    unique_id=unique_id,
                    example_index=example_index,
                    doc_span_index=doc_span_index,
                    tokens=tokens,
                    token_to_orig_map=token_to_orig_map,
                    token_is_max_context=token_is_max_context,
                    input_ids=input_ids,
                    input_mask=input_mask,
                    segment_ids=segment_ids,
                    start_position=final_start_positions,
                    end_position=final_end_positions,
                    is_impossible=is_impossible,
                )
            )
            unique_id += 1

    return features

def read_brat(datadir, ans_set=None, haslabels=True):
    """ Reads select examples annotated with brat. Examples are filtered by the answers in answer set
    Agruments:
        datadir {string} -- path to folder containing all annotation files and raw txt files
        ans_set {set{string}} -- set of answers to consider. None means consider all {Default=None} 
    Returns
        list{SESExample} -- returns list of SESExample Objects
    """
    examples = []
    all_files = os.listdir(datadir)
    txt_files = []
    ann_files = []
    for f in all_files:
        if f.endswith(".txt"):
            txt_files.append(f)
        elif f.endswith(".ann"):
            ann_files.append(f)
    for f in txt_files:
        file_name = f[:-4]
        ann_file = file_name + ".ann"
        if ann_file in ann_files:

            ann_f = open(os.path.join(datadir, ann_file), "r")
            txt_f = open(os.path.join(datadir, f), "r")

            ans_list = []
            if haslabels:
                for line in ann_f.readlines():
                    try:
                        line = line.split("\t")
                        index_and_labels = line[1]
                    except:
                        raise Exception(line, ann_file)
                    ans_type = index_and_labels.split()[0]
                    if ans_set is None or ans_type in ans_set:
                        # Add to answer list
                        text = line[2]
                        num_leading_ws = len(text) - len(text.lstrip())
                        ans_list.append(
                            SESAnswer(
                                text=text.strip(),
                                ans_type=ans_type,
                                start_char=int(index_and_labels.split()[1])
                                + num_leading_ws,
                            )
                        )
            examples.append(
                SESExample(text=txt_f.read(), text_id=file_name, ans_list=ans_list)
            )
        else:
            logging.info("No corresponding .ann file for %s" % f)

    return examples


def get_brat_examples(datadir, classes=None, min_num_answers_per_paper=1, haslabels=True):
    """Gets a list of SESExamples given a brat directory.
        Note: Directory must have .txt and corresponding .ann files if it has labels

    Args:
        datadir (str): Path to brat data directory
        classes (list{str}, optional): List of labels to keep. None means keep all. Defaults to None.
        min_num_answers_per_paper (int, optional): Don't keep papers with less than this number of labels . Defaults to 1.
        haslabels (bool, optional): Whether or not the brat directory has labels (.ann files). Defaults to True.

    Returns:
        list{SESExamples}: The list of SESExamples built from the brat data
    """

    examples = read_brat(datadir, classes, haslabels=haslabels)

    if haslabels:
        examples = [ex for ex in examples if len(ex.ans_list) >= min_num_answers_per_paper]

    return examples

def filter_features(features, ans_type_list):
    """DEPRICATED: Allow user to specify this in config. Only here for reference.
    """
    final_features = []
    for f in features:
        contains_answer = False
        for i, ans in enumerate(ans_type_list):
            if not f.is_impossible[i]: 
                contains_answer = True
                break
        if contains_answer and f.start_position != [[0]] and f.end_position != [[0]]:
            final_features.append(f)

    return final_features


def get_all_ans_types_from_examples(examples):
    """Get unique list of answers found in all the examples

    Args:
        examples (list{SESExample}): The list of SESExamples

    Returns:
        list{str}: The list of possible answers found in the examples
    """
    answers = []
    for e in examples:
        answers.extend([ans for ans in e.ans_list if ans not in answers])
    
    return answers