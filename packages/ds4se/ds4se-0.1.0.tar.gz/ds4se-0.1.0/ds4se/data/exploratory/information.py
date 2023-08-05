# AUTOGENERATED! DO NOT EDIT! File to edit: dev/08_data.exploratory.information.ipynb (unless otherwise specified).

__all__ = ['get_cnts', 'encode_text', 'get_dist', 'get_entropies_from_docs', 'get_entropy_from_docs',
           'get_doc_entropies_from_df', 'get_corpus_entropies_from_df', 'get_system_entropy_from_df',
           'shared_cnts_from_docs', 'shared_entropy_from_docs', 'shared_entropy_from_df', 'get_shared_probs_from_docs']

# Cell
# Imports
import dit
import os

import matplotlib.pyplot as plt
import pandas as pd
import sentencepiece as sp

from collections import Counter
from pathlib import Path
from scipy.stats import sem, t
from statistics import mean, median, stdev

# ds4se
from ..preprocessing import *

# Cell
def get_cnts(toks):
    cnt = Counter()
    for tok in toks:
        cnt[tok] += 1

    return cnt

# Cell
def encode_text(text, model_prefix):
    '''Encodes text using a pre-trained sp model, returns the occurrences of each token in the text'''
    sp_processor = sp.SentencePieceProcessor()
    sp_processor.Load(f"{model_prefix}.model")
    encoding = sp_processor.encode_as_pieces(text)

    token_counts = get_cnts(encoding)
    return token_counts

# Cell
def get_dist(token_counts):
    '''Takes in a counter object of token occurrences, computes the entropy of the corpus that produced it'''
    num_tokens = sum(token_counts.values())
    outcomes = list(set(token_counts.elements()))
    frequencies = []
    for token in token_counts:
        frequencies.append((token_counts[token])/num_tokens)

    return dit.ScalarDistribution(outcomes, frequencies)

# Cell
def get_entropies_from_docs(docs):
    entropies = []
    for doc in docs:
        token_counts = get_cnts(doc)
        entropies.append(dit.shannon.entropy(get_dist(token_counts)))

    return entropies

# Cell
def get_entropy_from_docs(docs):
    entropies = []
    token_counts = Counter()
    for doc in docs:
        token_counts += get_cnts(doc)

    return dit.shannon.entropy(get_dist(token_counts))

# Cell
def get_doc_entropies_from_df(df, col, model_path, data_types):
    '''Returns a list of the entropies of each entry in a dataframe column'''
    all_entropies = []
    for data_type in data_types:
        corpus = df.loc[df['data_type'] == data_type]
        entropies = []
        for data in corpus[col]:
            token_counts= encode_text(data, model_path)
            entropies.append(dit.shannon.entropy(get_dist(token_counts)))

        all_entropies.append(entropies)

    return all_entropies

# Cell
def get_corpus_entropies_from_df(df, col, model_path, data_types):
    entropies = []
    for data_type in data_types:
        corpus = df.loc[df['data_type'] == data_type]
        token_counts = Counter()
        for data in corpus[col]:
            token_counts += encode_text(data, model_path)
        entropies.append(dit.shannon.entropy(get_dist(token_counts)))

    return entropies

# Cell
def get_system_entropy_from_df(df, col, model_path):
    token_counts = Counter()
    for data in df[col]:
        token_counts += encode_text(data, model_path)

    return dit.shannon.entropy(get_dist(token_counts))

# Cell
def shared_cnts_from_docs(sys_docs):
    cnts = []
    for docs in sys_docs:
        token_counts = Counter()
        for doc in docs:
            token_counts += get_cnts(doc)
        cnts.append(token_counts)

    return cnts

# Cell
def shared_entropy_from_docs(sys_docs):
    cnts = shared_cnts_from_docs(sys_docs)
    overlap = set(cnts[0])
    for i, cnt in enumerate(cnts[1:]):
        overlap &= set(cnt)

    overlap = Counter({k: sum(cnts, Counter()).get(k, 0) for k in list(overlap)})
    return dit.shannon.entropy(get_dist(overlap))

# Cell
def shared_entropy_from_df(df, col, model_path, data_types):
    cnts = []
    for data_type in data_types:
        corpus = df.loc[df['data_type'] == data_type]
        token_counts = Counter()
        for data in corpus[col]:
            token_counts += encode_text(data, model_path)
        cnts.append(token_counts)

    overlap = set(cnts[0])
    for i, cnt in enumerate(cnts[1:]):
        overlap &= set(cnt)

    overlap = Counter({k: sum(cnts, Counter()).get(k, 0) for k in list(overlap)})
    return dit.shannon.entropy(get_dist(overlap))

# Cell
def get_shared_probs_from_docs(sys_docs):
    cnts = shared_cnts_from_docs(sys_docs)