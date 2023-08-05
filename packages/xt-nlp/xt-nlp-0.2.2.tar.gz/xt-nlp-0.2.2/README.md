# xt-nlp

## Description

This repo contains common NLP pre/post processing functions, loss functions, metrics, and helper functions.

## Installation

From PyPI:
```bash
pip install xt-nlp
```

From source:
```bash
git clone https://github.com/XtractTech/xt-nlp.git
pip install ./xt-nlp
```

## Usage

See specific help on a class or function using `help`. E.g., `help(SESLoss)`.

#### Defining SES Metrics and Loss
```python
from xt_nlp.metrics import SESF1
from xt_nlp.metrics import SESLoss

eval_metrics = {
   'f1': SESF1(threshold=0.8)
}
loss_fn = SESLoss()
```

#### Read BRAT annotations for sequence extraction into data loader
```python
from xt_nlp.utils import get_brat_examples, split_examples, get_features, build_ses_dataloader

# tokenizer = 
# max_sequence_length = 
# doc_stride =
# class_dict = Dictionary mapping classname ==> list of classes to group into this class
# classes = 
# batch_size = 
# workers = 

examples = get_brat_examples(
    datadir='./data/datadir',
    classes=classes
)

train_examples, val_examples = split_examples(examples, train_prop=.9, seed=4000)

train_features = get_features(
    examples=train_examples, 
    tokenizer=tokenizer, 
    all_ans_types=classes, 
    max_seq_len=max_sequence_length,
    doc_stride=doc_stride,
    mode='train'
)

train_loader = build_ses_dataloader(
    train_features, 
    classes, 
    class_dict, 
    batch_size=batch_size,
    workers=workers,
    max_seq_length=max_sequence_length,
    shuffle=True
)
```



