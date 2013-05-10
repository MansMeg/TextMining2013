# -*- coding: utf-8 -*-
"""
@author: Måns Magnuson och Leif Jonsson
"""

# Preparations
import nltk
from random import shuffle, seed
# from Labb5Functions import my_classify_results,document_features_b,document_features_a
# from string import punctuation
# from re import sub, search
# from nltk.corpus import stopwords
# nltk.download()

# Functions is in a separate file 

# Read in data
from nltk.corpus import movie_reviews
reviews = [(list(movie_reviews.words(fileid)), category)
            for category in movie_reviews.categories()
            for fileid in movie_reviews.fileids(category)]
seed(20130510)
shuffle(reviews)

# Part A
# We use the code from the example in the book
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_feat = all_words.keys()[:1000]

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

# Different types of normalizing is tried with the data
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


# Part C
# We use the same code as above
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_feat = all_words.keys()[:1000]

# Feature set (using b)
featureset = [(document_features_b(d,word_feat,contain_wrd=True), c) for (d,c) in reviews]
# Feature set is devided in train, dev and test sets
train_set, dev_set, test_set = featureset[600:],featureset[400:600], featureset[:400]
classifier_b = nltk.NaiveBayesClassifier.train(train_set)

# Classifying the dev set
test_classifed = [classifier_b.classify(fs[0]) for fs in test_set]
test_true = [fs[1] for fs in test_set]

# Calculating accuracy, precision etc.
print my_classify_results(test_true,test_classifed)
# Classification rate
#Accuracy : 0.515
#Precision : 0.5
#Recall : 0.613402061856
#F-value : 0.550925925926

#The classification rate is much worse when including counts when using the naive
#bayesian classifier where only "more than one" were included as an third category.
#
#The reason for this is that the naive classifier have problems when there are lot 
#of rare events and these rare events is distorting the results rather than improving
#the bayesian classifier.
# It is difficult to correct this for every single document.


# Part D)
# The same problem as with the earlier
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_feat = all_words.keys()[0:10000]
tdfidf_dict = idf(reviews,word_feat) # Approx 30 seconds when word_feat = 10k

# Biggest difference in idftf between categories, can be seen as cosine "non"-similarity
term_dict = {}
result = []
for term in word_feat:
    term_dict[term] = [0,0]
    for doc_no in range(len(reviews)):
        if reviews[doc_no][1]=="neg":
            term_dict[term][0] = term_dict[term][0] + tdfidf_dict[str(doc_no)][term]
        else:
            term_dict[term][1] = term_dict[term][1] + tdfidf_dict[str(doc_no)][term]
    result.append([abs(term_dict[term][0]-term_dict[term][1]),term])

result = sorted(result,reverse = True)
word_feat = [word[1] for word in result[0:50]]
featureset = [(document_features_a(d,word_feat), c) for (d,c) in reviews]
train_set, dev_set, test_set = featureset[600:],featureset[400:600], featureset[:400]
classifier_d = nltk.NaiveBayesClassifier.train(train_set)

# Classifying the test set
test_classifed = [classifier_d.classify(fs[0]) for fs in test_set]
test_true = [fs[1] for fs in test_set]
# Calculating accuracy, precision etc.
print my_classify_results(test_true,test_classifed)

#Accuracy : 0.7125
#Precision : 0.715846994536
#Recall : 0.675257731959
#F-value : 0.694960212202

# Part E
# read in negative and positive words only
import os
os.getcwd()
raw_pos = open("TextMining2013/L5/OpinLex/positive-words.txt").read()
raw_neg = open("TextMining2013/L5/OpinLex/negative-words.txt").read()
pos_set = set(raw_pos.split("\n"))
neg_set = set(raw_neg.split("\n"))

# Feature set is created
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_feats = all_words.keys()[:1000]
featureset = [(document_features_posneg(d,pos_set,neg_set), c) for (d,c) in reviews]
#featureset = [(document_features_posneg(d,pos_set,neg_set,contain_word=True,word_feat=word_feats), c) for (d,c) in reviews]

# Feature set is devided in train, dev and test sets
train_set, dev_set, test_set = featureset[600:],featureset[400:600], featureset[:400]
classifier_posneg = nltk.NaiveBayesClassifier.train(train_set)

# Classifying the test set
test_classifed = [classifier_posneg.classify(fs[0]) for fs in test_set]
test_true = [fs[1] for fs in test_set]
print my_classify_results(test_true,test_classifed)


