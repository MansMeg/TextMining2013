# -*- coding: utf-8 -*-
"""
Created on Tue May 7 11:02:31 2013
@author: Måns Magnuson och Leif Jonsson
"""

# Preparations
import nltk
from random import shuffle
# nltk.download()

# Functions 
def my_classify_results(true_values,classified_values):
    cm = nltk.ConfusionMatrix(true_values, classified_values)
    tp,tn = cm.__getitem__(("pos","pos")),cm.__getitem__(("neg","neg"))
    fp,fn = cm.__getitem__(("neg","pos")),cm.__getitem__(("pos","neg"))
    allres = tp+fp+tn+fn
    precision = tp / (tp+fp)
    recall = tp / (tp+fn)
    return "Accuracy : %s\nPrecision : %s\nRecall : %s\nF-value : %s" % ((tp+tn)/allres, precision, recall, 2*precision*recall/(precision+recall))


# Part A
from nltk.corpus import movie_reviews

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

# Classifying the test set
test_classifed = [classifier_a.classify(fs[0]) for fs in test_set]
test_true = [fs[1] for fs in test_set]

# Calculating accuracy, precision etc.
print my_classify_results(test_true,test_classifed)
#Accuracy : 0.805
#Precision : 0.836734693878
#Recall : 0.780952380952
#F-value : 0.807881773399



