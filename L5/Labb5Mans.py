# -*- coding: utf-8 -*-
"""
Created on Tue May 7 11:02:31 2013
@author: Måns Magnuson och Leif Jonsson
"""

# Preparations
import nltk
from re import sub, search
from random import shuffle, seed
from nltk.corpus import stopwords
from string import punctuation
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

def document_features_a(document,word_feat):
    document_words = set(document)
    features = {}
    for word in word_feat:
        features['contains(%s)' % word] = (word in document_words)
    return features



# Part A
from nltk.corpus import movie_reviews
reviews = [(list(movie_reviews.words(fileid)), category)
            for category in movie_reviews.categories()
            for fileid in movie_reviews.fileids(category)]
seed(20130510)
shuffle(reviews)

# We use the code from the example in the book
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = all_words.keys()[:1000]

# Feature set is created
featureset = [(document_features_a(d,word_feat), c) for (d,c) in reviews]
# Feature set is devided in train, dev and test sets
train_set, dev_set, test_set = featureset[600:],featureset[400:600], featureset[:400]
classifier_a = nltk.NaiveBayesClassifier.train(train_set)

# Classifying the test set
test_classifed = [classifier_a.classify(fs[0]) for fs in test_set]
test_true = [fs[1] for fs in test_set]

# Calculating accuracy, precision etc.
print my_classify_results(test_true,test_classifed)
#Accuracy : 0.7525
#Precision : 0.741116751269
#Recall : 0.752577319588
#F-value : 0.746803069054


# Part B
# The same data should be used as above
porter = nltk.PorterStemmer()
wnl = nltk.WordNetLemmatizer()
word_reviews = movie_reviews.words()


# Different types of normalizing is tied on the data
# Porter stemming:
# word_reviews = [porter.stem(word.lower()) for word in word_reviews]
# Lemmatizing:
# word_reviews = [wnl.lemmatize(word.lower()) for word in word_reviews]
# Removing punctuation etc:
# rmset = set(stopwords.words('english'))
# rmset.update([p for p in punctuation])
# rmset.update("")
# word_reviews = [sub("\W","",word).lower() for word in word_reviews if not search('^\W+$', word)]
# word_reviews = [word for word in word_reviews if word not in rmset]

# Choosing features
all_words = nltk.FreqDist(w for w in word_reviews)
word_featb = all_words.keys()[:1000]

# Feature set is created
featureset = [(document_features_a(d,word_featb), c) for (d,c) in reviews]
train_set, dev_set, test_set = featureset[600:],featureset[400:600], featureset[:400]
classifier_b1 = nltk.NaiveBayesClassifier.train(train_set)

# Classifying the test set
test_classifed = [classifier_b1.classify(fs[0]) for fs in test_set]
test_true = [fs[1] for fs in test_set]
print my_classify_results(test_true,test_classifed)

# Results by removing punctuations etc (all docs have punctuations)
#Accuracy : 0.7725
#Precision : 0.766839378238
#Recall : 0.762886597938
#F-value : 0.764857881137

# Conclution
#By excluding numbers, stopwords and punctuations the classifier is slightly
#better, but only marginally (from an accuracy of 0.7525 to 0.7725). 
#
#We also tried if lemmatizing or stemming could increase the classification 
#accuracy, but doing this just reduced the classification accuracy.
# 
#It is quite hard to improve the classification accuracy by different types
#of normalizing methods, even if the number of features is doubled from
#1000 to 2000 the accuracy is only increased to 0.79 from 0.7525. 

