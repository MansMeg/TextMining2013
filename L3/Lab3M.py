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
raw = re.sub("(\s)\s+","\1",raw)
raw = re.sub("[\t\r\x01]","\n",raw)
raw


