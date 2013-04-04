# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:33:20 2013

@author: mansmagnusson
"""

# Import libaries
import re
import random
#dir(random)

# 1
# (a) Define the variable
parrot = "It is dead, that is what is wrong with it."
# (b) Count the number of characters (letters, blank space, commas, 
# periods etc) in the sentence.
len(parrot)
#help(map)
#help(re.findall)
#help('lambda')

char = len(re.findall("[A-Za-z]",parrot))
blanks = len(re.findall(" ",parrot))
dots = len(re.findall("\.",parrot))
decimal = len(re.findall(",",parrot))
print "There are %s characters, %s blanks, %s commas and %s punctuation" \
 % (char,blanks,decimal,dots)

# (c) Write code that counts the number of letters in the sentence.
# w word constituence. \W
char = len(re.findall("\w",parrot))
print "There are %s chars in parrot" % char

# (d) Separate the sentence into a list of words. Call the list ParrotWords.
# ?split(parrot)
ParrotWords = parrot.split()

# (e) Merge (concatenate) ParrotWords into a sentence again.
print "Parrot splitted and joined: %s" % " ".join(ParrotWords)


# 3
# (a) Write a for loop that produces the following output on the screen:
# The next number in the loop is 5
# The next number in the loop is 6
# ...
# The next number in the loop is 10
# [Hint: the range() function has more than one argument].
#help(range)
for i in range(4,10):
    print "The next number in the loop is %d" % (i + 1) 

# (b) Write a while-loop that repeatedly generates a random number from a 
# uniform distribution over the interval [0;1] , and prints the sentence 
# ’The random number is smaller than 0:9’ on the screen until 
# the generated random number is smaller than 0:9. 
# [Hint: Python has a random module with basic random number generators].

ranNum = random.random()
while ranNum < 0.9:
    print "The random number is in 0:0.9 (%s)" % (ranNum) 
    ranNum = random.random()


# (c) Write a for-loop that iterates over the list
# names = [’Ludwig’,’Rosa’,’Mona’,’Amadeus’]
# and writes the following to the screen:
# The name Ludwig is nice
# The name Rosa is nice
# ...
# The name Amadeus is nice
# Use Python’s string formatting capabilities (the %s stuff ...) to solve 
# the problem.

names = ["Ludwig","Rosa","Mona","Amadeus"]
for name in names:
    print "The name %s is nice" % (name) 
    
#help(format)
#help("%")
# (d) Write a for-loop that iterates over the list
# names = [’Ludwig’,’Rosa’,’Mona’,’Amadeus’] and produces the list
# nLetters = [6,4,4,7] that counts the letters in each name.
# [Hint: the pretty version uses the enumerate() function]

names = ["Ludwig","Rosa","Mona","Amadeus"]
nLetters = map(len,names)

nLetters = []
for name in names:
    nLetters.append(len(name))
    
# (e) Solve the previous question using a list comprehension.
nLetters = [len(x) for x in names]

# (f) Use a list comprehension to produce a list that indicates if 
# the name has more than four letters. The answer should be
# shortLong = [’long’,’short’,’short’,’long’].
def ourFun(text):
    if len(text)<5:
        res = "long"
    else:
        res = "short"
    return res

shortLong = [ourFun(text) for text in names]
shortLong = ["long" if len(text)>=5 else "short" for text in names ]

# (g) Write a loop that simultaneously loops over the lists names and
# shortLong to write the following to the screen
# The name Ludwig is a long name
# The name Rosa is a short name
# ...
# The next Amadeus is a long name
# [Hint: use the zip() function and Python’s string formatting.
#help(zip)
for name in zip(names,shortLong):
    print "The name %s is a %s name" % name


# 3. Dictionaries
# (a) Make a dictionary named Amadeus containing the information that the 
# student Amadeus is a male (M), scored 8 on the Algebra exam and 13 on the 
# History exam.

Amadeus = {"sex":"M","History":8,"Algebra":8}

# (b) Make three more dictionaries, one for each of the students: Rosa, 
# Mona and Ludwig, from the information in the following table:
Rosa = {"sex":"F","History":19,"Algebra":22}
Mona = {"sex":"F","History":6,"Algebra":27}
Ludwig = {"sex":"M","History":9,"Algebra":5}

# (c) Combine the four students in a dictionary named students such that a 
# user of your dictionary can type students[’Amadeus’][’History’] to retrive 
# Amadeus score on the history test. [HINT: The values in a dictionary can be
# dictionaries]

students = {"Amadeus":Amadeus,"Rosa":Rosa,"Mona":Mona,"Ludwig":Ludwig}
students

# (d) Add the new student Karl to the dictionary students. Karl scored 14 
# on the Algebra exam and 10 on the History exam.

students["Karl"] = {"sex":"M","History":10,"Algebra":14}

# (e) Use for-loop to print out the names and scores of all students on
# the screen. The output should look like something this (the order of the 
# students doesn’t matter):
# Student Amadeus scored 8 on the Algebra exam and 13 on the History exam 
# Student Rosa scored 19 on the Algebra exam and 22 on the History exam
# ...
# [Hints: Dictionaries are iterables. A really pretty solution involves 
# the .items() method of a dictionary]
#help(dict.items)
#dir(dict)
for output in students.items():
    print "Student %s scored %d on the Algebra exam and %d on the Histry exam"\
    % (output[0],output[1]["History"],output[1]["Algebra"])


# 4. Vectors and arrays
# (a) Define two lists: list1 = [1,3,4] and list2 = [5,6,9]. Try 
# list1*list2. Does it work?
list1 = [1,3,4]
list2 = [5,6,9]
# list1*list2
print "list1*list1 does not work, since the '*' operator is not overridden for \
lists"
# Nope, the above does not work

# (b) Import everything from scipy (from scipy import *). Convert list1 
# and list2 into arrays (name them array1 and array2). Now try array1*array2.
import scipy as sp
array1 = sp.array(list1)
array2 = sp.array(list2)
print "array * array is = %s" % (array1 * array2)

import numpy as nu
# (c) Let matrix1 be a 2-by-3 array with array1 and array2 as its two 
# rows. Let matrix2 be a diagonal matrix with elements 1, 2 and 3. 
# Try matrix1*matrix2. Why doesn’t this work?
matrix1 = nu.array([list1,list2])
matrix2 = nu.diag([1,2,3])
#nu.multiply(matrix1,matrix2)
print "Multiplying matrix1 and matrix2 does not work since matrix1 is not \
a matrix, only an array "
# It multiply elementwise
print matrix1
print matrix2
type(matrix1)
type(matrix2)

# (d) Compute the usual matrix product of matrix1 and matrix2.
import numpy as np
print "np.dot(matrix1,matrix2) = %s" % np.dot(matrix1,matrix2)
print "(np.matrix(matrix1) * matrix2) = %s" % (np.matrix(matrix1) * matrix2)
print "numpy overrides the '*' operator for matrices"

# 5. Functions
# (a) Write a function CircleArea(radius) that computes the area of a 
# circle with radius radius. Call the function to show that it works. 
# [Hint: the number π needs to be loaded from the math module]

def area(radius):
    from math import pi
    return radius**2*pi

print "Area(-3) = %s" % area(-3)

# (b) Modify the CircleArea function so that it checks it the radius is 
# positive and prints The radius must be positive to the screen if it 
# is not. Also, if the radius is not positive the function should return None.

def area(radius):
    if radius<0:
        return None
    else:
        from math import pi
        return radius**2*pi

print "Area(-3) = %s" % area(-3)

# (c) Now write another function RectangleArea(base,height) that computes the 
# area of a rectangle. Put both functions in a text file named Geometry.py. 
# Close the Python interpreter (or all of Spyder, if you prefer). Start the 
# interpreter and load the two area functions from the module.

from geometry import area, RectangleArea
import geometry

# (d) Now define another function in your Geometry module that computes the 
# area of a triangle. Try to import the new function from the module. Why 
# does it not work? [Hint: try import imp followed by imp.reload(Geometry)]
import os
os.getcwd()
reload(geometry)
print "Triangle area(2,3) = %s " % geometry.Triangle(2.4,3.5)
#help(reload)
