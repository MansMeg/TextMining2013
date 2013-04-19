# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 15:12:00 2013

@author: mansmagnusson
"""

import nltk
from urllib import urlopen
import re


# Part 1)
url = "http://www.guardian.co.uk/politics/2013/apr/08/iron-lady-margaret-thatcher"
html = urlopen(url).read()
raw = nltk.clean_html(html)

raw = open("/Users/mansmagnusson/Desktop/Text Mining/Labs/TextMining2013/L3/thatcher.txt").read()

raw = re.sub("[\t\r]","",raw)
raw = re.sub("\|"," ",raw)
raw = re.sub(" +"," ",raw)
raw = re.sub("\n+","\n",raw)
raw = re.sub("( \n)+"," \n",raw)

raw = nltk.clean_html(html)
raw = re.sub("\|"," ",raw)
raw = re.sub("(\s)\s+","\1",raw)
raw = re.sub("[\t\r\x01\n]",".\n ",raw)



# Part 2)
# Segmenting
sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
sents = sent_tokenizer.tokenize(raw)
# Normalizing (stemming and lemming)
porter = nltk.PorterStemmer()
wnl = nltk.WordNetLemmatizer()
Tokens = sentToken = sentTokenStem = sentTokenLem = []
for sentence in sents:
    token = nltk.word_tokenize(sentence)
    tokenStem = [porter.stem(t) for t in token]
    lemmas = [wnl.lemmatize(t) for t in token]
    sentToken.append(token)
    sentTokenStem.append(tokenStem)
    sentTokenLem.append(lemmas)
    Tokens = Tokens + token


# Part 3)
POS = []
stemPOS = []
for sentence in sentToken:
    POS.append(nltk.pos_tag(sentence))
for sentence in sentTokenStem:
    stemPOS.append(nltk.pos_tag(sentence))

# This has been done manually, see report.

# Part 4)
ner_tag = []
ner_tag_stem = []
for sentence in POS:
    ner_tag.append(nltk.ne_chunk(sentence))

for sentence in stemPOS:
    ner_tag.append(nltk.ne_chunk(sentence))

help(nltk.ne_chunk)
