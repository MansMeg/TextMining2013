'''
Created on Apr 27, 2013

First skeleton of and Indexer that builds an inverted index

@author: Leif Jonsson & Mans Magnusson
'''

import os
import nltk

basedir = os.path.dirname(os.path.realpath(__file__))

basedir = basedir + "/texts/"
texts = os.listdir(basedir)

index = {}

for text in enumerate(texts):
    raw = open(basedir + text[1]).read()
    tokens = nltk.word_tokenize(raw.lower())
    for token in tokens:
        if token in index:
            index[token] = {"tf":(index[token]["tf"]+1), "docs":list(set(index[token]["docs"]+[text[0]]))}
        else:
            index[token] = {"tf":1, "docs":[text[0]]}
            
for token in index.keys():
    print "{0} => {1}".format(token,index[token])