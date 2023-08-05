import numpy as np
from tqdm import tqdm
import os 
import importlib
import argparse
import collections 
import torch
import logging

from transformers import BertTokenizer

from xt_training import Runner
from xt_models.models import BertForSES

from .postprocessing import get_results
from .datasets import build_ses_dataloader
from .preprocessing import get_features
from ..metrics import SESLoss, SESRecall

logger = logging.getLogger()
logger.setLevel(logging.INFO)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def infer(s, model=None, tokenizer=None, examples=None, features=None):
    """Runs SES inference and returns the outputs for each class

    Args:
        s (config): The config file
        model (model, optional): The model. Defaults to None.
        tokenizer (tokenizer, optional): The tokenizer. Defaults to None.
        examples (list{SESExample}, optional): The SES Examples to convert to SESFeature. Defaults to None.
        features (list{SESFeature}, optional): The list of SESFeatures to run. Defaults to None.

    Raises:
        Exception: Currenly only batch_size of 1 is supported.

    Returns:
        list{OrderedDict}: List of length nclasses with extracted sequences.
    """
    # Load Model and Tokenizer
    if not model:
        if hasattr(s, 'model'):
            model = s.model
        else:
            assert hasattr(s, 'model_path')
            model = BertForSES.from_pretrained(
                s.model_path,
                num_ans_types=len(s.class_dict),
            )
    model.eval()
    model.to(device)

    if not tokenizer:
        if hasattr(s, 'tokenizer'):
            tokenizer = s.tokenizer
        else:
            assert hasattr(s, 'model_path')
            tokenizer = BertTokenizer.from_pretrained(s.model_path)

    # Load data
    logging.info("          loading data...")

    if not features:
        assert examples is not None
        features = get_features(
            examples=examples, tokenizer=tokenizer, all_ans_types=s.class_dict, max_seq_len=s.max_sequence_length,
            doc_stride=s.doc_stride, mode='test'
        )

    loader = build_ses_dataloader(
        features, 
        classes=s.classes, 
        class_dict=s.class_dict, 
        batch_size=s.batch_size,
        workers=s.workers,
        max_seq_length=s.max_sequence_length,
        shuffle=False, 
        has_labels=False
    )
    # Define model runner
    runner = Runner(
        model, 
        device=device
    )
    logging.info("          running model...")

    y_pred, y = runner(loader, 'test', return_preds=True)

    # Done for each batch start logits and end logits
    
    RawResult = collections.namedtuple("RawResult",
                                   ["unique_id", "start_logits", "end_logits"])
    all_results = []
    for i in range(len(s.class_dict)):
        all_results.append([])
    
    # infer outputs is (nbatches, 2, batch_size, seq_length, num_ans_types)
    # Need to reshape it to (nbatches*batch_size, seq_length, num_ans_types)
    
    assert s.batch_size == 1  # 'For inference, Batch size must be 1'

    for batch_ind, output in enumerate(y_pred):
        # start_logits,end_logits=output
        start_logits = output[0]
        end_logits = output[1]

        start_logits = start_logits.squeeze(0).permute(1, 0)
        end_logits = end_logits.squeeze(0).permute(1, 0)
        
        for class_idx, (out_s, out_e) in enumerate(zip(start_logits, end_logits)):

            start_output = out_s.detach().cpu().tolist()
            end_output = out_e.detach().cpu().tolist()

            eval_feature = features[batch_ind] #batchsize is 1 so this matches
            unique_id = int(eval_feature.unique_id)

            all_results[class_idx].append(RawResult(
                unique_id = unique_id,
                start_logits = start_output,
                end_logits = end_output
            ))

    # Remove -1 values from the all_results feature for empty text
    # flat_list = [item for sublist in all_results for item in sublist]
    # raise Exception(np.unique([x.unique_id for x in flat_list], return_counts=True)[1] == 1)
    # Get results for one feature
    all_outputs = []
    for class_idx, all_class_results in enumerate(all_results):
        output = get_results(
            s,
            all_class_results,
            examples,
            features,
            list(s.class_dict.keys())[class_idx]
        )
        all_outputs.append(output)

    return all_outputs