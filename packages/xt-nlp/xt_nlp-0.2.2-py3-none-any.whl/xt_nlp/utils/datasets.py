import numpy as np
import sys
import os
import pickle
import torch
from torch.utils.data import Dataset, DataLoader

class SESDataset(Dataset):
    """Simple in-RAM Dataset that allows tuples of inputs and labels
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        return len(self.x[0])

    def __getitem__(self, idx):
        
        x_item = list(zip(*self.x))[idx]
        y_item = list(zip(*self.y))[idx]

        return (x_item, y_item)


def build_ses_dataloader(
    features, 
    classes, 
    class_dict, 
    batch_size=1,
    workers=4,
    max_seq_length=384,
    shuffle=True, 
    has_labels=True
):

    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
    all_start_positions = torch.zeros(
        [
            len(features), 
            max_seq_length, 
            len(class_dict)
        ], 
        dtype=torch.float
    )
    all_end_positions = torch.zeros_like(all_start_positions)
    
    if has_labels:
        for j, feature in enumerate(features):
            for i in range(0, max_seq_length):
                for k, key in enumerate(class_dict):
                    for lab in class_dict[key]:
                        if i in feature.start_position[classes.index(lab)]: 
                            all_start_positions[j, i, k] = 1.0
                        if i in feature.end_position[classes.index(lab)]:
                            all_end_positions[j, i, k] = 1.0
    

    x = (all_input_ids,all_input_mask,all_segment_ids)
    y = (all_start_positions,all_end_positions)

    dataset = SESDataset(x, y)

    loader = DataLoader(
        dataset,
        num_workers=workers,
        batch_size=batch_size,
        shuffle=shuffle
    )

    return loader
