import math
import os
import collections
import numpy as np
import torch
import pickle

from transformers import BasicTokenizer



### Math
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def one_mult(text):
    """Any rescaling of answer scores based on text length
    
    Arguments:
        text {str} -- The predicted answer
    
    Returns:
        float -- The rescaling factor of the prediction score
    """

    return 1.0 # No rescaling

def _get_best_indexes(logits, n_best_size):
    """Get the n-best logits from a list."""

    index_and_score = sorted(enumerate(logits), key=lambda x: x[1], reverse=True)

    best_indexes = []
    for i in range(len(index_and_score)):
        if i >= n_best_size:
            break
        best_indexes.append(index_and_score[i][0])
    return best_indexes


def _compute_softmax(scores):
    """Compute softmax probability over raw logits."""
    if not scores:
        return []

    max_score = None
    for score in scores:
        if max_score is None or score > max_score:
            max_score = score

    exp_scores = []
    total_sum = 0.0
    for score in scores:
        x = math.exp(score - max_score)
        exp_scores.append(x)
        total_sum += x

    probs = []
    for score in exp_scores:
        probs.append(score / total_sum)
    return probs


def get_final_text(pred_text, orig_text, do_lower_case, verbose_logging=False):
    """Project the tokenized prediction back to the original text."""

    # When we created the data, we kept track of the alignment between original
    # (whitespace tokenized) tokens and our WordPiece tokenized tokens. So
    # now `orig_text` contains the span of our original text corresponding to the
    # span that we predicted.
    #
    # However, `orig_text` may contain extra characters that we don't want in
    # our prediction.
    #
    # For example, let's say:
    #   pred_text = steve smith
    #   orig_text = Steve Smith's
    #
    # We don't want to return `orig_text` because it contains the extra "'s".
    #
    # We don't want to return `pred_text` because it's already been normalized
    # (the SQuAD eval script also does punctuation stripping/lower casing but
    # our tokenizer does additional normalization like stripping accent
    # characters).
    #
    # What we really want to return is "Steve Smith".
    #
    # Therefore, we have to apply a semi-complicated alignment heruistic between
    # `pred_text` and `orig_text` to get a character-to-charcter alignment. This
    # can fail in certain cases in which case we just return `orig_text`.

    def _strip_spaces(text):
        ns_chars = []
        ns_to_s_map = collections.OrderedDict()
        for (i, c) in enumerate(text):
            if c == " ":
                continue
            ns_to_s_map[len(ns_chars)] = i
            ns_chars.append(c)
        ns_text = "".join(ns_chars)
        return (ns_text, ns_to_s_map)

    # We first tokenize `orig_text`, strip whitespace from the result
    # and `pred_text`, and check if they are the same length. If they are
    # NOT the same length, the heuristic has failed. If they are the same
    # length, we assume the characters are one-to-one aligned.
    tokenizer = BasicTokenizer(do_lower_case=do_lower_case)

    tok_text = " ".join(tokenizer.tokenize(orig_text))

    start_position = tok_text.find(pred_text)
    if start_position == -1:
        if verbose_logging:
            info("Unable to find text: '%s' in '%s'" % (pred_text, orig_text))
        return orig_text
    end_position = start_position + len(pred_text) - 1

    (orig_ns_text, orig_ns_to_s_map) = _strip_spaces(orig_text)
    (tok_ns_text, tok_ns_to_s_map) = _strip_spaces(tok_text)

    if len(orig_ns_text) != len(tok_ns_text):
        return orig_text

    # We then project the characters in `pred_text` back to `orig_text` using
    # the character-to-character alignment.
    tok_s_to_ns_map = {}
    for (i, tok_index) in tok_ns_to_s_map.items():
        tok_s_to_ns_map[tok_index] = i

    orig_start_position = None
    if start_position in tok_s_to_ns_map:
        ns_start_position = tok_s_to_ns_map[start_position]
        if ns_start_position in orig_ns_to_s_map:
            orig_start_position = orig_ns_to_s_map[ns_start_position]

    if orig_start_position is None:
        return orig_text

    orig_end_position = None
    if end_position in tok_s_to_ns_map:
        ns_end_position = tok_s_to_ns_map[end_position]
        if ns_end_position in orig_ns_to_s_map:
            orig_end_position = orig_ns_to_s_map[ns_end_position]

    if orig_end_position is None:

        return orig_text

    output_text = orig_text[orig_start_position : (orig_end_position + 1)]
    return output_text

def correct_start_and_end(start_index, end_index, final_text, example_text, window_size=20):
    
    # all_matches = list(re.finditer(final_text, example_text))
    # closest_match = all_matches.sort(key=lambda x: abs(x.start() - start_index))[0]
    
    # s_ind = closest_match.start()
    # e_ind = closest_match.end()

    start = 0
    start_indices = []

    ws_split = "".join([" " if c.isspace() else c for c in example_text])
    full_ws_split = " ".join(example_text.split())
    char_to_orig = {}
    orig_i = 0
    for i in range(len(full_ws_split)):
        if full_ws_split[i] != ws_split[orig_i]:
            while True:
                orig_i += 1
                if full_ws_split[i] == ws_split[orig_i]:
                    break
            char_to_orig[i] = orig_i
        else:
            char_to_orig[i] = orig_i


    while True:
        start = full_ws_split.find(final_text, start)
        if start == -1:
            break
        start_indices.append(start)
        start += len(final_text) 

    start_indices.sort(key=lambda x: abs(x - start_index))
    if len(start_indices) == 0:
        raise Exception(final_text, example_text[start_index - 10: end_index + 10])
    new_start = start_indices[0]
    new_end = new_start + len(final_text)

    orig_doc_start = char_to_orig[new_start]
    if new_end in char_to_orig:
        orig_doc_end = char_to_orig[new_end]
    else:
        orig_doc_end = char_to_orig[new_end-1]

    final_text = example_text[orig_doc_start:orig_doc_end]
    # raise Exception(new_start, new_end, char_to_orig[new_start], char_to_orig[new_end])


    return final_text, orig_doc_start, orig_doc_end


def get_results(s, class_results, all_examples, all_features, class_name, find_new_prob=one_mult):
    
    n_best_size = s.n_best_predictions
    max_answer_length = s.max_answer_length[class_name]
    prediction_threshold = s.prediction_thresholds[class_name]

    example_index_to_features = collections.defaultdict(list)
    # This maps example index --> list of features associated with that example
    for feature in all_features:
        example_index_to_features[feature.example_index].append(feature)
    
    unique_id_to_result = {}
    for result in class_results:
        unique_id_to_result[result.unique_id] = result

    _PrelimPrediction = collections.namedtuple(  # pylint: disable=invalid-name
        "PrelimPrediction",
        ["feature_index", "start_index", "end_index", "start_logit", "end_logit"],
    )

    all_predictions = collections.OrderedDict()
    all_nbest_json = collections.OrderedDict()
    for (example_index, example) in enumerate(all_examples):

        ##getting doc_tokens

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

        assert doc_tokens == example.whitespace_tokens

        features = example_index_to_features[example_index]
        prelim_predictions = []
        for (feature_index, feature) in enumerate(features):
            result = unique_id_to_result[feature.unique_id]

            start_indexes = _get_best_indexes(result.start_logits, n_best_size)
            end_indexes = _get_best_indexes(result.end_logits, n_best_size)
            #TODO: Test pmc31702679 . Why is the first 'hemiplegic shoulder pain' not being considered? even though the h has a high SL value?
            for start_index in start_indexes:
                for end_index in end_indexes:
                    # We could hypothetically create invalid predictions, e.g., predict
                    # that the start of the span is in the question. We throw out all
                    # invalid predictions.
                    if start_index >= len(feature.tokens):
                        continue
                    if end_index >= len(feature.tokens):
                        continue
                    if start_index not in feature.token_to_orig_map:
                        continue
                    if end_index not in feature.token_to_orig_map:
                        continue
                    if not feature.token_is_max_context.get(start_index, False):
                        continue
                    if end_index < start_index:
                        continue
                    length = end_index - start_index + 1
                    if length > max_answer_length:
                        continue
                    if sigmoid(result.start_logits[start_index]) + sigmoid(result.end_logits[end_index]) < prediction_threshold * 2:#s.measure_threshold: # Break if the answer is worse than our measure threshold
                        continue
                    prelim_predictions.append(
                        _PrelimPrediction(
                            feature_index=feature_index,
                            start_index=start_index,
                            end_index=end_index,
                            start_logit=result.start_logits[start_index],
                            end_logit=result.end_logits[end_index],
                        )
                    )

        _NbestPrediction = collections.namedtuple(
            "NbestPrediction", 
                ["text", 
                "start_logit", 
                "end_logit", 
                "start_index",
                "end_index",
                "orig_start_index", 
                "orig_end_index",
                "pred_section_start_char",
                "example_index",
                "feature_index"]
        )

        seen_predictions = {}
        nbest = []
        for pred in prelim_predictions:
            feature = features[pred.feature_index]

            tok_tokens = feature.tokens[pred.start_index : (pred.end_index + 1)]
            orig_doc_start = feature.token_to_orig_map[pred.start_index]
            orig_doc_end = feature.token_to_orig_map[pred.end_index]
            orig_tokens = doc_tokens[orig_doc_start : (orig_doc_end + 1)]

            tok_text = " ".join(tok_tokens)

            # Back out position of start of prediction in original section text
            #TODO: CHECK THIS LOGIC!
            num_whitespace_token_char_before_pred_start = 0
            for i in range(0, orig_doc_start):
                num_whitespace_token_char_before_pred_start += len(example.whitespace_tokens[i])

            section_text_pred_start_char = example.ws_token_char_to_string_char[num_whitespace_token_char_before_pred_start]

            # De-tokenize WordPieces that have been split off.
            tok_text = tok_text.replace(" ##", "")
            tok_text = tok_text.replace("##", "")

            # Clean whitespace
            tok_text = tok_text.strip()
            tok_text = " ".join(tok_text.split())
            orig_text = " ".join(orig_tokens)

            do_lower_case = getattr(s, 'do_lower_case', True)
            final_text = get_final_text(tok_text, orig_text, do_lower_case, False)


            # raise Exception(len(tok_text),tok_text, len(orig_text),orig_text ,char_to_word_offset.index(orig_doc_start), len(char_to_word_offset)-char_to_word_offset[::-1].index(orig_doc_end) - 1)
            seen_predictions[final_text] = True
            start_index=char_to_word_offset.index(orig_doc_start)
            if orig_doc_end + 1 in char_to_word_offset:
                end_index=char_to_word_offset.index(orig_doc_end+1) - 1
            else:
                # Very end of document
                end_index = len(char_to_word_offset) - 1


            final_text, start_index, end_index = correct_start_and_end(start_index, end_index, final_text, example.text)

            nbest.append(
                _NbestPrediction(
                    text=final_text,
                    start_logit=pred.start_logit,
                    end_logit=pred.end_logit,
                    start_index=start_index,
                    end_index=end_index,
                    orig_start_index=orig_doc_start, 
                    orig_end_index=orig_doc_end,
                    pred_section_start_char = section_text_pred_start_char,
                    example_index=example_index,
                    feature_index=pred.feature_index
                )
            )

            # raise Exception(final_text,char_to_word_offset.index(orig_doc_start),char_to_word_offset[::-1].index(orig_doc_end))
        # In very rare edge cases we could have no valid predictions. So we
        # just create a nonce prediction in this case to avoid failure.
        if not nbest:
            nbest.append(
                _NbestPrediction(
                    text="empty", 
                    start_logit=0.0, 
                    end_logit=0.0, 
                    start_index=0.0, 
                    end_index=0.0,
                    orig_start_index=0, 
                    orig_end_index=0,
                    pred_section_start_char = 0,
                    example_index=example_index,
                    feature_index=0
                )
            )

        nbest = stack_predictions(nbest) # Stack predictions to avoid overlapping!

        assert len(nbest) >= 1

        total_scores = []
        for entry in nbest:
            total_scores.append((entry.start_logit + entry.end_logit) * find_new_prob(entry.text))

        # no softmax
        probs = total_scores

        nbest_json = []
        for (i, entry) in enumerate(nbest):
            output = collections.OrderedDict()
            output["text"] = entry.text
            # print(entry.text)
            output["probability"] = probs[i]
            output["start_index"] = entry.start_index
            output["end_index"] = entry.end_index
            output["orig_start_index"] = entry.orig_start_index
            output["orig_end_index"] = entry.orig_end_index
            output["start_logit"] = entry.start_logit
            output["end_logit"] = entry.end_logit
            output["pred_section_start_char"] = entry.pred_section_start_char
            output["example_index"] = entry.example_index
            output["feature_index"] = entry.feature_index


            nbest_json.append(output)

        assert len(nbest_json) >= 1
        # if example.text_id == "17621027":
        # print("debugger")
        # all_predictions[example.text_id] = nbest_json[0]["text"]
        
        # all_nbest_json[example.text_id] = nbest_json #TODO: Check this [example] stuff
        if example.text_id:
            all_nbest_json[example.text_id] = nbest_json
        else:
            all_nbest_json[example] = nbest_json

    return all_nbest_json

def stack_predictions(preds_list):
    """
    Stack predictions.
    """
    preds_list.sort(key= lambda x: (x.start_index, len(x.text)))

    stacked_preds_list = []

    for stacked1 in preds_list:            
        stacked_preds_list = stack_item(stacked1, stacked_preds_list)

    # Sort again by score
    stacked_preds_list.sort(key=lambda x: x.start_logit + x.end_logit, reverse=True)

    return stacked_preds_list 

def stack_item(stacked1, stacked_preds_list):
    """Compares a prediction with all the stacked predictions so far and stacks if there is overlap
    
    Arguments:
        stacked1 {json} -- The prediction to stack
        stacked_preds_list {list{json}} -- All stacked predictions so far
    
    Returns:
        list{json} -- The stacked predictions after stacking the item
    """
    for stacked2_i, stacked2 in enumerate(stacked_preds_list):
        if stacked1.start_index < stacked2.end_index:
            # Stacked1 overlaps with Stacked2
            # First - keep whichever one does not have a newline
            if '\n' in stacked2.text and '\n' not in stacked1.text:
                stacked_preds_list[stacked2_i] = stacked1
            elif '\n' in stacked1.text and '\n' not in stacked2.text:
                pass
            else:
                # No newlines in either
                if stacked1.start_logit + stacked1.end_logit > stacked2.start_logit + stacked2.end_logit:
                    # Overwrite it with more confident answer
                    #TODO: Maybe keep the shorter one? Or Check For Overlapping?
                    stacked_preds_list[stacked2_i] = stacked1
            break
    
    else:
        # Exited without getting stacked
        stacked_preds_list.append(stacked1)

    return stacked_preds_list

def save_results(s, full_all_json_nbest, ans_type_list, examples, features, epoch_num):

    for ans_i, ans in enumerate(ans_type_list):
        results_file = os.path.join(
            s.output_dir, "results_" + str(ans) + "_enum" + str(epoch_num) + ".txt"
        )
        with open(results_file, "w") as f:
            for dict_i in full_all_json_nbest[ans_i]:
                # find index of example from unique id
                example_text_ids = [e.text_id for e in examples]
                ex_index = example_text_ids.index(dict_i)
                example = examples[ex_index]

                """
                feature_ids = [feature.unique_id for feature in features]
                feat_index = feature_ids.index(dict_i)
                ex_index = feature[feat_index].example_index
                example = examples[ex_index]
                """
                f.write("text: " + str(example.text) + "\n")
                f.write("Ground Truth Answers: \n")
                for k, true_ans in enumerate(example.ans_list):
                    if ans_type_list.index(true_ans.ans_type) == ans_i:
                        f.write(str(true_ans.text) + "\n")

                for j in range(0, 10):
                    if len(full_all_json_nbest[ans_i][dict_i]) > j:
                        f.write(
                            format(full_all_json_nbest[ans_i][dict_i][j]["probability"], ".10f")
                            + " "
                            + format(full_all_json_nbest[ans_i][dict_i][j]["start_logit"], ".10f")
                            + " "
                            + format(full_all_json_nbest[ans_i][dict_i][j]["end_logit"], ".10f")
                            + " "
                            + str(full_all_json_nbest[ans_i][dict_i][j]["text"])
                            + "\n"
                        )
                f.write(str("\n"))

