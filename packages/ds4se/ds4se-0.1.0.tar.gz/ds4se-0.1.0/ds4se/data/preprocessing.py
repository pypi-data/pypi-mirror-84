# AUTOGENERATED! DO NOT EDIT! File to edit: dev/00_data.preprocessing.ipynb (unless otherwise specified).

__all__ = ['jsonl_list_to_dataframe', 'get_dfs', 'df_to_txt_file', 'sp_model_from_df', 'sp_model_from_glob',
           'gen_hugface_model', 'tokenize_fns', 'read_bpe_files', 'split_lines_to_files']

# Cell
# Imports
import pandas as pd
import sentencepiece as sp

from pathlib import Path
from tokenizers import ByteLevelBPETokenizer
from tokenizers.processors import BertProcessing

# Cell
def jsonl_list_to_dataframe(file_list, columns=None):
    """Load a list of jsonl.gz files into a pandas DataFrame."""
    return pd.concat([pd.read_json(f,
                                   orient='records',
                                   compression='gzip',
                                   lines=True)[columns]
                      for f in file_list], sort=False)

# Cell
def get_dfs(path):
    """
        Grabs the different data splits and converts them into dataframes.
        Expects format from Code Search Net Challenge.
    """
    dfs = []
    for split in ["train", "valid", "test"]:
        files = sorted((path/split).glob("**/*.gz"))
        df = jsonl_list_to_dataframe(files, ["code", "docstring"])
        dfs.append(df)

    return dfs

# Cell
def df_to_txt_file(df, output, cols):
    """Converts a dataframe and converts it into a text file that SentencePiece can use to train a BPE model"""
    if cols is None: cols = list(df.columns)
    merged_df = pd.concat([df[col] for col in cols])

    with open(output/'text.txt', 'w') as f:
        f.write('\n'.join(list(merged_df)))
    return output/'text.txt'

# Cell
def sp_model_from_df(df, output, model_name, cols = None):
    """Trains a SentencePiece BPE model from a pandas dataframe"""
    fname = df_to_txt_file(df, output, cols)
    sp.SentencePieceTrainer.train(f'--input={fname} --model_prefix={output / model_name} --hard_vocab_limit=false')

# Cell
def sp_model_from_glob(path, glob, model_name):
    fns = list(path.glob(glob))
    fns = ",".join(map(str, fns))
    sp.SentencePieceTrainer.train(f'--input={fns} --model_prefix={path / model_name} --hard_vocab_limit=false')

# Cell
def gen_hugface_model(df, output, tokenizer = ByteLevelBPETokenizer(), vocab_sz = 30_000, min_freq = 3, cols = None):
    fname = df_to_txt_file(df, output, cols)
    tokenizer.train(files = [str(fname)], vocab_size = vocab_sz, min_frequency = min_freq, special_tokens=[
        "<s>",
        "<pad>",
        "</s>",
        "<unk>",
        "<mask>",
    ])

    return tokenizer

# Cell
def tokenize_fns(fns, tokenizer, exts, output, data_type):
    docs = []
    for fn in fns:
        system = fn.parent.name
        output_path = output/system/data_type
        output_path.mkdir(parents=True, exist_ok=True)
        files = []
        for ext in exts:
            files.extend(fn.glob(f'**/*.{ext}'))
        for file in files:
            if 'README' not in file.name:
                with open(file, encoding='ISO-8859-1') as f:
                    docs.append(tokenizer.EncodeAsPieces(f.read()))
                with open((output_path/file.name).with_suffix('.bpe'), 'w') as f:
                    f.write(' '.join(docs[-1]))

    return docs

# Cell
def read_bpe_files(path):
    bpe_files = []
    for file in path.glob('**/*.bpe'):
        with open(file) as f:
            bpe_files.append(f.read().split(' '))

    return bpe_files

# Cell
def split_lines_to_files(lines, fn_pattern, output_path, tokenizer):
    for line in lines:
        fn, content = line.split(fn_pattern)
        fn = fn.replace('"', '')
        fn = fn.replace(' Test ', '')
        content = tokenizer.EncodeAsPieces(content)
        with open((output_path/fn).with_suffix('.bpe'), 'w') as f:
                    f.write(' '.join(content))