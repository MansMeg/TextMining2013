'''
Created on Apr 27, 2013

First skeleton of and Indexer that builds an inverted index

@author: Leif Jonsson & Mans Magnusson
'''

import os
import nltk
import re
from collections import defaultdict

basedir = os.path.dirname(os.path.realpath(__file__))

basedir = basedir + "/texts/"
texts = os.listdir(basedir)

index = {}

porter = nltk.PorterStemmer()
for text in enumerate(texts):
    raw = open(basedir + text[1]).read()
    tokens = nltk.word_tokenize(raw.lower())
    tokens = [re.sub("[-*.='/+]", "",t) for t in tokens]
    tokens = [porter.stem(t) for t in tokens]
    for token in tokens:
        if token in index:
            d = index[token]["tf"]
            d[text[0]] += 1
        else:
            d = defaultdict(int)
            d[text[0]] = 1
        index[token] = {"tf":d}
            
for token in sorted(index.keys()):
    print "{0} => {1}".format(token,index[token])