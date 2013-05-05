# -*- coding: utf-8 -*-
"""
Created on Sat May  4 16:21:12 2013

@author: mansmagnusson
"""

# Read in documents as a list (for indexing)
import os
from collections import defaultdict
from nltk import word_tokenize,PorterStemmer
from re import search,sub
from os import listdir
import math

def read_doc(data_dir,stem=True):
    texts = listdir(data_dir)
    os.chdir(data_dir)
    doc_list = []
    for text in enumerate(texts):
        raw = open(text[1]).read()
        doc_list.append(clean_and_tokenize(raw,stem))
    return doc_list

def clean_and_tokenize(raw,stem=True):
    """(str) -> list"""
    tokens = word_tokenize(raw)
    tokens = [sub("\W","",word).lower() for word in tokens if not search('^\W+$', word)]
    if stem:
        tokens = [PorterStemmer().stem(token) for token in tokens]    
    return tokens

def inv_index(data):
    """list of list -> dict"""
    inv_index = defaultdict(list)
    for doc in enumerate(data):
        docset = set(doc[1])
        for token in docset:
            inv_index[token].append(str(doc[0]))
    return inv_index

def calc_tfs_dict(data):
    tfs_dict = {}
    for text in enumerate(data):
        tfs_dict[str(text[0])]=defaultdict(float)
        for word in text[1]:
            tfs_dict[str(text[0])][word] += 1
    return tfs_dict



def wtd(t,tfs_dict,inv_index,N,query=False):
    wtd_dict = defaultdict(float)
    if not query:
        docs = inv_index[t]
    else:
        docs = ["q"]
    for d in docs:
        wtd_dict[d] = (1+math.log(tfs_dict[d][t]))*math.log(N/len(inv_index[t]))
    return wtd_dict

def cosine_query(query,k,inv_index,tfs_dict,N,stem=True):
    token_q = clean_and_tokenize(query,stem)
    docs = set()
    term_dict = {}
    q_dict = {}
    tfs_dict["q"] = defaultdict(float)
    scores = {}
    for t in token_q:
        tfs_dict["q"][t] += 1
        docs.update(inv_index[t])
        term_dict[t] = wtd(t,tfs_dict,inv_index,N)
        q_dict[t] = wtd(t,tfs_dict,inv_index,N,query=True)["q"]
    for d in docs:
        cross = q2 = d2 = 0
        for t in token_q:
            cross += term_dict[t][d]*q_dict[t]
            q2 += q_dict[t]
            d2 += term_dict[t][d]
        scores[d] = cross/(q2*d2)
    return sorted(scores, key=scores.get, reverse=True)[0:k]
        
        
    
help(set)


# Run program
data_dir = "/Users/mansmagnusson/Desktop/Text Mining/Labs/TextMining2013/L4/texts"
data = read_doc(data_dir,stem=True)
inv_index = inv_index(data)
tfs_dict = calc_tfs_dict(data)
query = "cars demons races"
cosine_query(query,3,inv_index,tfs_dict,len(data),stem=True)
