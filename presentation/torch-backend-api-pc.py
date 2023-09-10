from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

import os
import json
import collections
import re
import jieba
import math
import torch
from torch import nn
import random
import pandas as pd
import numpy as np
import torch.nn as nn
import torch.utils.data as Data
from collections import OrderedDict
from tqdm import tqdm

# 函数部分
def seg_text(texts):
    seg_setence = []
    for text in texts:
        seg_setence.append(["" + ' '.join(list(jieba.cut(i, cut_all=False))) for i in text])
    return seg_setence
def tokenize(lines, token='word'):

    if token == 'word':
        return [i.split() for line in lines for i in line]

    elif token == 'char':
        return [list(i) for line in lines for i in line]

    else:
        print('错位：未知令牌类型：' + token)
class Vocab:

    def __init__(self, tokens=None, min_freq=0, reserved_tokens=None):

        if tokens is None:
            tokens = []

        if reserved_tokens is None:
            reserved_tokens = []

        counter = count_corpus(tokens)

        self.token_freqs = sorted(counter.items(), key=lambda x: x[1], reverse=True)

        uniq_tokens = reserved_tokens

        uniq_tokens += [token for token, freq in self.token_freqs
                        if freq >= min_freq and token not in uniq_tokens]

        self.idx_to_token, self.token_to_idx = [], dict()

        for token in uniq_tokens:
            self.idx_to_token.append(token)

            self.token_to_idx[token] = len(self.idx_to_token) - 1

    def __len__(self):

        return len(self.idx_to_token)

    def __getitem__(self, tokens):

        if not isinstance(tokens, (list, tuple)):
            return self.token_to_idx.get(tokens, self.unk)
        return [self.__getitem__(token) for token in tokens]

    def to_tokens(self, indices):

        if not isinstance(indices, (list, tuple)):
            return self.idx_to_token[indices]
        return [self.idx_to_token[index] for index in indices]
def count_corpus(tokens):
    if len(tokens) == 0 or isinstance(tokens[0], list):
        tokens = [token for line in tokens for token in line]

    return collections.Counter(tokens)
def make_data(tokens):
    enc_input_all, dec_input_all, dec_output_all = [], [], []

    for idx, token in enumerate(tokens):
        padded_token = token + ['<pad>'] * (n_step - len(token))

        if idx % 2 == 0:  # 奇数次循环
            enc_input = [letter2idx[n] for n in (padded_token + ['<eos>'])]
            enc_input_all.append(np.eye(n_class)[enc_input])
        else:  # 偶数次循环
            dec_input = [letter2idx[n] for n in (['<bos>'] + padded_token)]
            dec_output = [letter2idx[n] for n in (padded_token + ['<eos>'])]
            dec_input_all.append(np.eye(n_class)[dec_input])
            dec_output_all.append(dec_output)

    # make tensor
    return torch.Tensor(enc_input_all), torch.Tensor(dec_input_all), torch.LongTensor(dec_output_all)
class TranslateDataSet(Data.Dataset):
    def __init__(self, enc_input_all, dec_input_all, dec_output_all):
        self.enc_input_all = enc_input_all
        self.dec_input_all = dec_input_all
        self.dec_output_all = dec_output_all

    def __len__(self): # 返回数据集长度
        return len(self.enc_input_all)

    def __getitem__(self, idx):
        return self.enc_input_all[idx], self.dec_input_all[idx], self.dec_output_all[idx]
def supplement(word):
    model.load_state_dict(torch.load('C:/Users/ranxi/Desktop/揭榜挑战赛/sentence-completion/best_model.pth'))
    model.eval()

    input_tokens = list(jieba.cut(word, cut_all=False))

    enc_input_all, dec_input_all = [], []
    input_indices = [letter2idx[token] for token in input_tokens]

    padded_input_indices = input_indices + [letter2idx['<pad>']] * (n_step - len(input_indices)) + [letter2idx['<eos>']]

    padded_input_indices = [letter2idx['<bos>']] + input_indices + [letter2idx['<pad>']] * (n_step - len(input_indices))

    enc_input_all.append(np.eye(n_class)[padded_input_indices])
    dec_input_all.append(np.eye(n_class)[padded_input_indices])
    torch.Tensor(enc_input_all)
    torch.Tensor(dec_input_all)
    enc_input, dec_input = torch.Tensor(enc_input_all), torch.Tensor(dec_input_all)

    enc_input, dec_input = enc_input.to(device), dec_input.to(device)
    hidden = torch.zeros(1, 1, n_hidden).to(device)

    output = model(enc_input, hidden, dec_input)

    predict = output.data.max(2, keepdim=True)[1]

    decoded = [vocab.to_tokens(idx) for idx in predict]

    if '<eos>' in decoded:
        translated = ''.join(decoded[:decoded.index('<eos>')])
    else:
        translated = ''.join(decoded)

    if not translated.endswith('。'):
        translated += '。'

    return translated.replace('<pad>', '')
class Seq2Seq(nn.Module):
    def __init__(self):
        super(Seq2Seq, self).__init__()
        self.encoder = nn.GRU(input_size=n_class, hidden_size=n_hidden, dropout=0.5) # encoder
        self.decoder = nn.GRU(input_size=n_class, hidden_size=n_hidden, dropout=0.5) # decoder
        self.fc = nn.Linear(n_hidden, n_class)

    def forward(self, enc_input, enc_hidden, dec_input):
        # enc_input(=input_batch): [batch_size, n_step+1, n_class]
        # dec_inpu(=output_batch): [batch_size, n_step+1, n_class]
        enc_input = enc_input.transpose(0, 1) # enc_input: [n_step+1, batch_size, n_class]
        dec_input = dec_input.transpose(0, 1) # dec_input: [n_step+1, batch_size, n_class]

        # h_t : [num_layers(=1) * num_directions(=1), batch_size, n_hidden]
        _, h_t = self.encoder(enc_input, enc_hidden)
        # outputs : [n_step+1, batch_size, num_directions(=1) * n_hidden(=128)]
        outputs, _ = self.decoder(dec_input, h_t)

        model = self.fc(outputs) # model : [n_step+1, batch_size, n_class]
        return model
def return_result():
    text = request.json['text']
    input_sentence = text
    next_sentence = supplement(input_sentence)
    return jsonify({
        'text': next_sentence,
    })

@app.route('/', methods=['POST'])
def complet():
    result=return_result()
    return result

if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    file_path = 'C:/Users/ranxi/Desktop/揭榜挑战赛/sentence-completion/truncated_setence.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        sentence_data = json.load(file)

    original_sentence, truncated_sentence, supplement_sentence = [], [], []
    for item in sentence_data:
        original_sentence.append(item["original_sentence"])
        truncated_sentence.append(item["truncated_sentence"])
        supplement_sentence.append(item["supplement_sentence"])

    seq_date = [[a, b] for a, b in zip(truncated_sentence, supplement_sentence)]
    jieba.load_userdict("C:/Users/ranxi/Desktop/揭榜挑战赛/sentence-completion/userdict.txt")
    segmented_setence = seg_text(seq_date)

    tokens = tokenize(segmented_setence)
    letter = [char for word in tokens for char in word]
    letter.append('<pad>')
    letter.append('<bos>')
    letter.append('<eos>')
    vocab = Vocab(letter, reserved_tokens=[' '])
    letter2idx = vocab.token_to_idx
    # Seq2Seq参数
    n_step = max(len(token) for token in tokens)
    n_hidden = 256
    n_class = len(letter2idx)  # n分类问题
    batch_size = 3
    enc_input_all, dec_input_all, dec_output_all = make_data(tokens)

    # Seq2Seq模型
    model = Seq2Seq().to(device)
    criterion = nn.CrossEntropyLoss().to(device)

    app.run(host='0.0.0.0', port=999)

