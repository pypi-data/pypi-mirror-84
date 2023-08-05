import torch
import torch.nn as nn
from functools import lru_cache
from sklearn.metrics import f1_score, precision_score, recall_score

from xt_training.metrics import PooledMean

class SESLoss:
    def __init__(self, hot_loss_mult=None, weight=None):
        self.hot_loss_mult = hot_loss_mult
        self.weight = weight
        self.loss_fn = nn.BCEWithLogitsLoss(weight=weight)
    
    def __call__(self, ypred, y):
        hot_loss = 0
        final_loss = 0
        start_logits, end_logits = ypred
        start_positions, end_positions = y
        if start_positions is not None and end_positions is not None:
            s_mask = start_positions == 1
            e_mask = end_positions == 1        
            
            # print(start_logits.shape, start_positions.shape)
            s_loss = self.loss_fn(start_logits, start_positions)
            e_loss = self.loss_fn(end_logits, end_positions)    
            loss = ((s_loss + e_loss) / 2)
            final_loss += loss        

            if self.hot_loss_mult and start_positions.sum() != 0 and end_positions.sum() != 0:
                # One hot loss
                s_hot_loss = self.loss_fn(start_logits[s_mask], start_positions[s_mask])
                e_hot_loss = self.loss_fn(end_logits[e_mask], end_positions[e_mask])    
                hot_loss = ((s_hot_loss + e_hot_loss) / 2)
                final_loss += hot_loss * self.hot_loss_mult
    
        return final_loss

# Metrics

@lru_cache(8)
def get_inputs(ypred, y, measure_threshold, index=None):
    start_logits, end_logits = ypred
    start_positions, end_positions = y
    sigmoid = nn.Sigmoid()

    start_logits = sigmoid(start_logits)
    end_logits = sigmoid(end_logits)
    start_logits = (start_logits > measure_threshold)[:,:,index].flatten().cpu()
    end_logits = (end_logits > measure_threshold)[:,:,index].flatten().cpu()
    start_positions = (start_positions == 1)[:,:,index].flatten().cpu()
    end_positions = (end_positions == 1)[:,:,index].flatten().cpu()

    return (start_logits, end_logits, start_positions, end_positions)


class SESF1:
    def __init__(self, threshold=0.5, index=None):
        self.threshold = threshold
        self.index = index
    
    def __call__(self, ypred, y):
        y = tuple(y)
        ypred = tuple(ypred)
        start_logits, end_logits, start_positions, end_positions = get_inputs(ypred, y, self.threshold, index=self.index)
        f1 = (f1_score(start_positions, start_logits, zero_division=1) + f1_score(end_positions, end_logits, zero_division=1)) / 2
        
        return torch.tensor(f1)

class SESPrecision:
    def __init__(self, threshold=0.5, index=None):
        self.threshold = threshold
        self.index = index
    
    def __call__(self, ypred, y):
        y = tuple(y)
        ypred = tuple(ypred)
        start_logits, end_logits, start_positions, end_positions = get_inputs(ypred, y, self.threshold, index=self.index)
        precision = (precision_score(start_positions, start_logits, zero_division=1) + precision_score(end_positions, end_logits, zero_division=1)) / 2
        
        return torch.tensor(precision)  
  
class SESRecall:
    def __init__(self, threshold=0.5, index=None):
        self.threshold = threshold
        self.index = index
    
    def __call__(self, ypred, y):
        y = tuple(y)
        ypred = tuple(ypred)
        start_logits, end_logits, start_positions, end_positions = get_inputs(ypred, y, self.threshold, index=self.index)
        recall = (recall_score(start_positions, start_logits, zero_division=1) + recall_score(end_positions, end_logits, zero_division=1)) / 2
        
        return torch.tensor(recall) 