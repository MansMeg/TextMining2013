from __future__ import division
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 05 07:15:41 2013

@author: Leif Jonsson & Måns Mangnusson
"""

from  scipy.stats import poisson

print "================ Assignment 1 ================"
print "\n=== A 1.1 ====\n"
mu = 4
nosamples = 100
X = poisson.rvs(mu,size=nosamples)
print "X = {0}".format(X)

print "\n=== A 1.2 ====\n"
mean = sum(X) / len(X)
print "mean = {0}".format(mean)
var  = (sum(map(lambda num: num**2,X)) / len(X)) - mean**2
print "var  = {0}".format(var) 

print "\n=== A 1.3 ====\n"
print "Theoretical mean of poisson (mu) = {0}".format(mu)
print "Theoretical var  of poisson (mu) = {0}".format(mu)

print "\n=== A 1.4 ====\n"
from collections import Counter
freqs = Counter(X)
print "Frequencies = {0}".format(freqs)

print "\n=== A 1.5 ====\n"
import matplotlib.pyplot as plt
x = [cnt[0] for cnt in freqs.items()]
print "Plotting bar chart with x = {0}".format(x)
y = [cnt[1] for cnt in freqs.items()]
print "Plotting bar chart with y = {0}".format(y)
plt.clf()
plt.bar(x,y)
plt.legend(y,loc='best')
plt.title("Frequencies")
plt.show()

print "\n=== A 1.6 ====\n"
vals = [poisson.pmf(Z,mu) for Z in range(14)]
print vals
plt.clf()
plt.bar(range(14),vals)
plt.title("Poisson PMF")
plt.show()    

print "\n=== A 1.7 ====\n"
from  scipy.stats import ttest_1samp
print "The probability that mu = 2.0 is {0:.4f}".format(ttest_1samp(X,2.0)[1])
print "The probability that mu = 3.7 is {0:.4f}".format(ttest_1samp(X,3.7)[1])
print "The probability that mu = 4.3 is {0:.4f}".format(ttest_1samp(X,4.3)[1])


print "\n\n\n================ Assignment 2 ================"
print "\n=== A 2.1 ====\n"
ssize = 100
from  scipy.stats import expon,norm
X1 = expon.rvs(scale=5,size=ssize)
X2 = expon.rvs(scale=5,size=ssize)
print X1
print X1

print "\n=== A 2.2 ====\n"
Y = ['Blue' if x1*x2<=(30.0+norm.rvs(1)) else 'Orange' for x1 in X1 for x2 in X2]

import numpy as np
h = .1
x_min, x_max = 0, max(X1)
y_min, y_max = 0, max(X2)
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))


print "\n=== A 2.3 ====\n"
print "Displaying scatter plot of generated values with colors from Y in A 2.2"
plt.clf()
plt.subplot(2, 2, 1)
plt.scatter(X1,X2,c=Y)
plt.title("Scatter plot of generated values")
print "The data is usually quite well separated"
#plt.show()

print "\n=== A 2.4 ====\n"
from sklearn import svm
Xes = zip(X1,X2)
Ys = [0 if x[0]*x[1]<=(30.0+norm.rvs(1)) else 1 for x in Xes]
print "True Ys"
print Ys

print "\n=== A 2.5.a ====\n"
clf = svm.SVC(kernel='linear')
clf.fit(Xes,Ys)
print clf

print "\n=== A 2.6.a ====\n"
slinpred = clf.predict(zip(xx.ravel(),yy.ravel()))
linpred = clf.predict(Xes)
print "Predicted using Linear kernel"
print linpred

print "\n=== A 2.5.b ====\n"
clf = svm.SVC(kernel='rbf',gamma=0.7)
clf.fit(Xes,Ys)
print clf


print "\n=== A 2.6.b ====\n"
srbfpred = clf.predict(zip(xx.ravel(),yy.ravel()))
rbfpred = clf.predict(Xes)
print "Predicted using RBF kernel"
print rbfpred

print "\n=== A 2.7.a ====\n"
print "Displaying scatter plot that compares linear svm vs. true values."
jitteroffset= 10
X1Jitter = norm.rvs(size=len(X1)) / jitteroffset
X2Jitter = norm.rvs(size=len(X2)) / jitteroffset
LinPredcols = ['Blue' if x==0 else 'Orange' for x in linpred]
#plt.clf()
plt.subplot(2, 2, 2)
plt.contourf(xx, yy, np.reshape(slinpred,xx.shape), cmap=plt.cm.Paired)
plt.scatter(X1,X2,c=Y)
plt.scatter(X1+X1Jitter,X2+X2Jitter,c=LinPredcols,cmap=plt.cm.Paired,marker='D')
plt.title("Scatter plot with predicted values (linear kernel jittered) vs. \
true values")
#plt.show()

print "\n=== A 2.7.b ====\n"
print "Displaying scatter plot that compares rbf svm vs. true values."
RBFPredcols = ['Blue' if x==0 else 'Orange' for x in rbfpred]
X1Jitter = norm.rvs(size=len(X1)) / jitteroffset
X2Jitter = norm.rvs(size=len(X2)) / jitteroffset
plt.subplot(2, 2, 3)
plt.contourf(xx, yy, np.reshape(srbfpred,xx.shape), cmap=plt.cm.Paired)
plt.scatter(X1,X2,c=Y)
plt.scatter(X1+X1Jitter,X2+X2Jitter,c=RBFPredcols,marker='D')
plt.title("Scatter plot with predicted values (rbf kernel jittered) vs. true\
 values")
#plt.show()


print "\n=== A 2.7.c ====\n"
print "Displaying scatter plot that compares rbf vs. linear vs. true values."
print "Conclusions: For this problem the RBF and Linear kernels has \
similar performance"

lcorrect = sum([1 if x1==x2 else 0 for x1 in linpred for x2 in Ys])
print "Correct predictions using Linear Kernel = {0} ({1}%)"\
.format(lcorrect, lcorrect/len(Ys))
rcorrect = sum([1 if x1==x2 else 0 for x1 in rbfpred for x2 in Ys])
print "Correct predictions using RBF Kernel    = {0} ({1}%)"\
.format(rcorrect, rcorrect/len(Ys))

plt.subplot(2, 2, 4)
plt.scatter(X1,X2,c=Y)
plt.scatter(X1+X1Jitter,X2+X2Jitter,c=LinPredcols,marker='D')
X1Jitter = norm.rvs(size=len(X1)) / jitteroffset
X2Jitter = norm.rvs(size=len(X2)) / jitteroffset
plt.scatter(X1+X1Jitter,X2+X2Jitter,c=RBFPredcols,marker='^')
plt.title("Scatter plot with predicted values (rbf+linear kernel jittered) vs.\
 true values")
plt.show()
