

class SESExample(object):
    """ Class designed for SES Examples.
    Attributes:
        'text':
            raw string representing the full text of the EBM example
        'text_id':
            a unique id (string or integer) representing the EBM example
        'ans_list':
            a list 0 or more SESAnswer objects
        'whitespace_tokens':
            a list of string representing the white space tokenization of the text
        'ws_token_char_to_string_char':
            a list of size whitespace_tokens with values corresponding to the indexes in the original text
    """

    def __init__(self, 
                text = None,
                section = None,
                para_index = None,
                text_id = None,
                ans_list = None,
                whitespace_tokens = None):
        self.text = text
        self.section = section
        self.para_index = para_index
        self.text_id = text_id
        self.ans_list = ans_list

        whitespace_tokens = []
        ws_map = []
        prev_is_whitespace = True
        string_index_count = 0
        for c in text:
            if c.isspace():
                prev_is_whitespace = True
            else:
                if prev_is_whitespace:
                    whitespace_tokens.append(c)
                    ws_map.append(string_index_count)
                else:
                    whitespace_tokens[-1] += c
                    ws_map.append(string_index_count)
                prev_is_whitespace = False
            string_index_count += 1
        self.whitespace_tokens = whitespace_tokens
        self.ws_token_char_to_string_char = ws_map


class SESAnswer(object):
    """ Class designed for a SES answer.
    Attributes:
        'text':
            raw text of answer
        'ans_type':
            string or integer identifier of ans_type
        'start_char':
            starting char index of answer in full EBM example text
            (i.e. "world" in "hello world" would have start_char 6)
    """  
    
    def __init__(self, 
                text = None,
                ans_type = None,
                start_char = None):
        self.text = text
        self.ans_type = ans_type
        self.start_char = start_char


class SESFeature(object):
    """ Class representing an SES feature.
    Attributes:
        'unique_id':
            a integer (above 1000000000) that identifies the feature
        'example_index'
            index of the example in the example list where the feature originated
        'doc_span_index':
            index of feature in the doc spans list for an example
        'tokens':
            list of test tokens
        'token_to_orig_map':
            maps tokens in doc span to tokens in original example sequence (i think) 
        'token_is_max_context':
            list of booleans for whether tokens are consider part of this example (for doc stride overlap) 
        'input_ids':
            list of indices of all tokens in vocabulary list
        'input_mask':
            list of masks for tokens (0=padding, 1=real tokens)
        'segment_ids': 
            list of segment id for tokens (0=A sentence, 1=B sentence)
        'start_position':
            list size ans_type of lists of all answer start token indices
        'end_position':
            list size ans_type of lists of all answer end token indices
        'is_impossible':
            list of size ans_type of booleans representing if answer exists 
    """
    def __init__(self,
                 unique_id,
                 example_index,
                 doc_span_index,
                 tokens,
                 token_to_orig_map,
                 token_is_max_context,
                 input_ids,
                 input_mask,
                 segment_ids,
                 start_position=None,
                 end_position=None,
                 is_impossible=None):
        self.unique_id = unique_id
        self.example_index = example_index
        self.doc_span_index = doc_span_index
        self.tokens = tokens
        self.token_to_orig_map = token_to_orig_map
        self.token_is_max_context = token_is_max_context
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.start_position = start_position
        self.end_position = end_position
        self.is_impossible = is_impossible
