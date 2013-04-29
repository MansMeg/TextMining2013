'''
Created on Apr 27, 2013

The postings in the Inverted index consists of a 
dictionary where keys are the document number and
the tf for for the token is the value

@author: Leif Jonsson & Mans Magnusson
'''

import os
import nltk
import re
from collections import defaultdict
import math

texts = []
porter = nltk.PorterStemmer()

basedir = os.path.dirname(os.path.realpath(__file__))
basedir = basedir + "/texts/"

def prune_token(token):
    return porter.stem(re.sub("[-*.='/+]", "",token))

def calc_inverted_index():
    global texts 
    global basedir
    texts = os.listdir(basedir)
    
    index = {}
    
    for text in enumerate(texts):
        raw = open(basedir + text[1]).read()
        tokens = nltk.word_tokenize(raw.lower())
        tokens = [prune_token(t) for t in tokens]
        for token in tokens:
            if token in index:
                d = index[token]
                d[text[0]] = d[text[0]]+1
            else:
                d = defaultdict(int)
                d[text[0]] = 1
            index[token] = d
    return index

def calc_query_tf(tokens):
    d = defaultdict(int)
    for token in tokens:
        if token in index:
            d[token] += 1
        else:
            d[token] = 1
    return d
        
index = calc_inverted_index()

for token in sorted(index.keys()):
    print "{0} => {1}".format(token,index[token])
    

def query_index(query,k):
    '''
    This is an implementation of the CosineScore(q) algorithm
    '''
    global index
    global texts
    tokens = nltk.word_tokenize(query.lower())
    tokens = [prune_token(t) for t in tokens]
    tfs = calc_query_tf(tokens)
    print "Tfs {0}".format(tfs)
    scores = defaultdict(int)
    N = len(texts)
    for t in set(tokens):
        # do calculate wt;q
        # and fetch postings list for t
        postings = index.get(t,{})
        #print "Postings for {0} => {1} ({2})".format(t, postings, type(postings))
        #for each pair(d; tft;d ) in postings list
        #do Scores[d]+ = wt;d  wt;q
        for doc in postings.items():
            dft = len(postings)
            #print "Tf of {0} in doc {1} is {2}".format(t,doc[0],doc[1])
            wtd = (1 + math.log(doc[1])) * math.log(N/dft)
            wtq = (1 + math.log(tfs[t])) * math.log(len(tokens)/1)
            scores[doc[0]] += wtd * wtq
            #print "Score of {0} is {1}".format(doc[0],scores[doc[0]])
    return sorted(scores, key=scores.get, reverse=True)[0:k]
            
def block_format(desc):
    newdesc = ""
    offset = 100
    subdesc = desc
    while len(subdesc) > offset:
        newdesc += "\t" + subdesc[:offset] + "\n";
        subdesc = subdesc[offset:]
    newdesc += "\t" + subdesc
    return newdesc

query = 'realistic car racing game from zynga with realistic cars from saab'
k = 10
score_sorted_texts = query_index(query,k)

print "Top {0} documents for query: {1}".format(k,query)
for index in enumerate(score_sorted_texts):
    print "{0} => {1}".format(index[0],texts[index[1]])
    desc = open(basedir + texts[index[1]]).read()
    print "{0}\n".format(block_format(desc))

    
