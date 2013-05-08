# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:02:31 2013

@author: mansmagnusson
"""

# Preparations
import nltk
nltk.download()

# Part one
from nltk.corpus import movie_reviews
from random import shuffle
reviews = [(list(movie_reviews.words(fileid)), category)
            for category in movie_reviews.categories()
            for fileid in movie_reviews.fileids(category)]
shuffle(reviews)

# We use the code from the example in the book
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = all_words.keys()[:1000]
def document_features_a(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

# Feature set is created
featureset_a = [(document_features_a(d), c) for (d,c) in reviews]
# Feature set is devided in train, dev and test sets
train_set, dev_set, test_set = featureset_a[600:],featureset_a[400:600], featureset_a[:400]
classifier_a = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier_a, test_set)

classifier_a.classify(dev_set)
classifier_a.classify

cm = nltk.ConfusionMatrix(gold, test)



all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
list(all_words)[0:2]
documents[0]
