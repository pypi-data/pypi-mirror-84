""" All general helper functions """
import os
import sys
import collections
import contextlib
import pickle
import math
from tqdm import tqdm
from xt_training import metrics
from functools import lru_cache
import torch
import torch.nn as nn

from sklearn.metrics import f1_score, precision_score, recall_score
import random 

from .ses_utils import SESFeature, SESAnswer, SESExample
from .statistics import print_example_stats, print_feature_stats

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Logger(object):

    def __init__(self, mode, length, epochs, progress_file=None):
        """Text logging class.

        Arguments:
            mode {str} -- Run mode, used as a prefix in log output (e.g., 'train' or 'valid').
            length {int} -- Length of training loop, generally the number of batches in an epoch
                (i.e., the length of the dataloader).
        """
        self.mode = mode
        self.length = length
        self.global_iteration = 0
        self.global_length = epochs * length
        self.progress_file = progress_file

    def __call__(self, loss, metrics, i):
        track_str = '\r{:8s} | {:5d}/{:<5d}| '.format(self.mode, i + 1, self.length)
        loss_str = 'loss: {:9.4f} | '.format(loss)
        metric_str = ' | '.join('{}: {:9.4f}'.format(k, v) for k, v in metrics.items())
        self.global_iteration += 1        
        logging.info(track_str + loss_str + metric_str + '   ')

        if self.progress_file:
            with open(self.progress_file, 'a') as f:
                f.write(str(int(((self.global_iteration)*100)/(self.global_length)))+"\n")
                f.flush()



### TQDM Utils
# class DummyTqdmFile(object):
#     """Dummy file-like that will write to tqdm."""

#     file = None

#     def __init__(self, file):
#         self.file = file

#     def write(self, x):
#         # Avoid # logging.info() second call (useless \n)
#         if len(x.rstrip()) > 0:
#             tqdm.write(x, file=self.file)

#     def flush(self):
#         return getattr(self.file, "flush", lambda: None)()


# @contextlib.contextmanager
# def std_out_err_redirect_tqdm():
#     """ Use 'with: std_out_err_redirect_tqdm()' before entering for loop using tqdm."""
#     orig_out_err = sys.stdout, sys.stderr
#     try:
#         sys.stdout, sys.stderr = map(DummyTqdmFile, orig_out_err)
#         yield orig_out_err[0]
#     # Relay exceptions
#     except Exception as exc:
#         raise exc
#     # Always restore sys.stdout/err if necessary
#     finally:
#         sys.stdout, sys.stderr = orig_out_err
