# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 15:12:00 2013

@author: mansmagnusson
"""

import nltk
from urllib import urlopen
import re
# from pprint import pprint
# pprint(locals())
# help("BASICMETHODS")


# Part 1)
url = "http://www.guardian.co.uk/politics/2013/apr/08/iron-lady-margaret-thatcher"
html = urlopen(url).read()
html[:60]

raw = nltk.clean_html(html)
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
porter = nltk.PorterStemmer()
sentToken = []
Tokens = []
for sentence in sents:
    token = nltk.word_tokenize(sentence)
    token = [porter.stem(t) for t in token]
    sentToken.append(token)
    Tokens = Tokens + token

# Tokens starting with capital letter
cleanToken = filter(lambda t: re.match("[A-Z]\w+",t) ,Tokens)

raw = re.sub("\|"," ",raw)
len(set(cleanToken))



# Part 3)
