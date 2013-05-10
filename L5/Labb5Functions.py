# -*- coding: utf-8 -*-
"""
@author: Måns Magnuson och Leif Jonsson
"""
from collections import Counter,defaultdict
from math import log
from nltk import ConfusionMatrix
from numpy import mean

def cut(to_cut,cut_values,max_val=None):
    """Divide values of to_cut into classes given by cut_values"""
    ret = []
    for obj in to_cut:
        maxed = True
        for cut in cut_values:
            if obj < cut:
                ret.append(cut)
                maxed = False
                break
        if maxed:
            ret.append(max_val)
    return ret

def my_classify_results(true_values,classified_values):
    cm = ConfusionMatrix(true_values, classified_values)
    tp,tn = cm.__getitem__(("pos","pos")),cm.__getitem__(("neg","neg"))
    fp,fn = cm.__getitem__(("neg","pos")),cm.__getitem__(("pos","neg"))
    print tp,tn,fp,fn
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

def document_features_d(document,word_feat,limit): # Do own tdfidf limit
    document_words = set(document)
    features = {}
    for word in word_feat:
        features['contains(%s)' % word] = (word in document_words)
    return features

# Analyzing quantiles for defining categories in featb function
#import numpy,scipy
#no_words = []
#word_mean = []
#for rev in reviews:
#    no_words.append(len(rev[0]))
#    word_mean.append(numpy.mean(map(len,rev[0])))
#scipy.stats.mstats.mquantiles(no_words)
#scipy.stats.mstats.mquantiles(word_mean)

# Read in sentiments:
#Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
#Proceedings of the ACM SIGKDD International Conference on Knowledge 
#Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
#Washington, USA


def document_features_b(document,word_feat,tdf_id_feat=False,tdf_id_dict={},contain_wrd=False):
    doc_len_cut = [560, 745, 958, 999]
    av_word_cut = [3.8,3.93,4.06,9]
    word_cnt_cut = [1,2,9]
    
    # Doc length (in words)
    len_doc = cut([len(document[0])],doc_len_cut[0:3],doc_len_cut[3])
    # Average word length in review
    av_word = cut([mean(map(len,document[0]))],av_word_cut[0:3],av_word_cut[3])
    
    if tdf_id_feat: # Word counts/tdf-idf
        word_cnt = tdf_id_dict
    else: # Count word
        word_cnt = Counter(document[0])
    
    # Compute features
    features = {}
    for part in doc_len_cut:
       features['doclen_(%s)' % part] = part == len_doc[0]
    
    for part in av_word_cut:
       features['avword_(%s)' % part] = part == av_word[0]
    
    if contain_wrd:
        document_words = set(document)
        for word in word_feat:
            features['contains(%s)' % word] = (word in document_words)
    else:
        for word in word_feat:
            wrd_cut = cut([word_cnt[word]],word_cnt_cut[0:(len(word_cnt_cut)-1)],word_cnt_cut[(len(word_cnt_cut)-1)])
            for part in word_cnt_cut:
                features['wrd(%s)(%s)' % (word, part)] = part == wrd_cut[0]    
    return features

def idf(doc_list,terms):
    cnt = Counter()
    tdf = {}
    w = {}
    for doc in enumerate(doc_list):
        doc_set = set(doc[1][0])
        cnt.update(doc_set.intersection(set(terms)))
        tdf[str(doc[0])] = Counter(doc_set.intersection(set(terms)))
        for key in tdf[str(doc[0])].keys():
            tdf[str(doc[0])][key] = 1 + log(tdf[str(doc[0])][key])
    for key in cnt.keys():
        cnt[key] = log(len(doc_list)/cnt[key])
    for doc_no in range(len(doc_list)):
        w[str(doc_no)] = defaultdict(float)
        for key in tdf[str(doc[0])].keys():
            w[str(doc_no)][key] = tdf[str(doc_no)][key] * cnt[key]
    return w


def document_features_posneg(document,pos_set,neg_set):
    word_cnt_cut = [11,15,18,22,25,29,32,38,45,999]
    #[   1.,   15.,   22.,   29.,   37.,  131.]
    #[  0.,  16.,  22.,  29.,  38.,  95.]
    pos_cnt = 0
    neg_cnt = 0    
    # Count pos/neg
    for word in document:
        if word in pos_set:
            pos_cnt += 1 
        if word in neg_set:
            neg_cnt += 1
    # Pos and neg count categories
    pos_cut = cut([pos_cnt],word_cnt_cut[0:-1],word_cnt_cut[-1])
    neg_cut = cut([neg_cnt],word_cnt_cut[0:-1],word_cnt_cut[-1])
    
    # Compute features
    features = {}
    for part in word_cnt_cut:
       features['pos_cut_(%s)' % part] = part == pos_cut[0]
       features['neg_cut_(%s)' % part] = part == neg_cut[0]
    
    return features #,pos_cnt,neg_cnt

# Debugging:
#pos = [document_features_posneg(document[0],pos_set,neg_set) for document in reviews]
#neg = [document_features_posneg(document[0],pos_set,neg_set)[1] for document in reviews]
#scipy.stats.mstats.mquantiles(pos,[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
#scipy.stats.mstats.mquantiles(neg,[0,0.2,0.4,0.6,0.8,1])
