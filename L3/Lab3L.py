import nltk, pprint
import re
import signal
import sys

stats = {}
posCorrectStemmedwords = 0
posCorrectUnStemmedwords = 0
nerCorrectStemmedwords = 0
nerCorrectUnStemmedwords = 0
nerCorrectStemmedWords = 0
nerCorrectUnStemmedWords = 0
totWords = 0


def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        result = "";
        result += "Correct POS Tagged on Stemmed Lowercase Words: {0}\n".format(posCorrectStemmedwords)
        result += "Correct POS Tagged on Unstemmed Lowercase Words: {0}\n".format(posCorrectUnStemmedwords)
        result += "Correct NER Tagged on Stemmed Lowercase Words: {0}\n".format(nerCorrectStemmedwords)
        result += "Correct NER Tagged on UnStemmed Lowercase Words: {0}\n".format(nerCorrectUnStemmedwords)
        result += "Correct NER Tagged on Stemmed Uppercase Words: {0}\n".format(nerCorrectStemmedWords)
        result += "Correct NER Tagged on UnStemmed Uppercase Words: {0}\n".format(nerCorrectUnStemmedWords)
        result += "Total Words: {0}".format(totWords)
        text_file = open("Results.txt", "w")
        text_file.write(result)
        text_file.close()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print 'Press Ctrl+C sometime...'

def askCorrect():
    ans = 'x'
    while ans not in ['Y','y','N','n']:
        ans = raw_input("Was chunk correct? [y|n]:")
        return True if(ans in ['Y','y']) else False

#from urllib import urlopen
#url = "http://www.guardian.co.uk/politics/2013/apr/08/iron-lady-margaret-thatcher"
#html = urlopen(url).read()
#text_file = open("scripts/Lab3/iron-lady-margaret-thatcher", "w")
#text_file.write(html)
#text_file.close()
#html = open("scripts/Lab3/iron-lady-margaret-thatcher").read()
#raw = nltk.clean_html(html)
#raw = open("/Users/lejon/Documents/workspace/TextMiningLabs/scripts/Lab3/thatcher_short.txt").read()
raw = open("/Users/lejon/Documents/workspace/TextMiningLabs/scripts/Lab3/thatcher_rest.txt").read()
#raw = open("thatcher_short.txt").read()
#print raw
#raw = h.unescape(raw)
#print raw
text = raw
#text = re.sub(r"(\s)\s+",r"\1",text)
text = re.sub("(\s|\n){2,}", ".\n", text)
text = re.sub(r"[ \t]+",r" ",text)
text = re.sub(r"^\s*$",r"",text,flags=re.MULTILINE)
text = re.sub(r"\r",r"",text)
punct = r"[-!\"#%&'()*,./:;?@[\\\]_{}\|]"
#text = re.sub(punct,"",text)
#text = re.sub(r"\n+",r".\n",text)
#print text

sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
sents = sent_tokenizer.tokenize(text)

pprint.pprint(sents)

for sentence in sents:
    words = nltk.word_tokenize(sentence.lower())
    Words = nltk.word_tokenize(sentence)
    totWords += len(words)
    wnl = nltk.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in words]
    # lemmatizitation only affects a few 's words
    #print zip(lemmas,words)
    porter = nltk.PorterStemmer()
    stemmedwords = [porter.stem(t) for t in words]
    #print stemmedWords
    #print zip(words,stemmedWords)
    posTagStemmedwords = nltk.pos_tag(stemmedwords)
    #print "POS Tagged Stemmed words"
    #print posTagStemmedwords
    text_file = open("posTagStemmedwords.txt", "a")
    result = ""
    for pos in posTagStemmedwords:
        result += pos.__str__() + "\n"
        print "result is {0}".format(result)
#        if not pos[0]==pos[1]:
#            print pos
#            if( askCorrect() ):
#                posCorrectStemmedwords += 1
    text_file.write(result)
    text_file.close()

    # Conclusion: POS tagging should probably be done BEFORE stemming since the result is different
    posTagUnStemmedwords = nltk.pos_tag(words)
    print "POS Tagged UnStemmed words"
    print posTagUnStemmedwords
    text_file = open("posTagUnStemmedwords.txt", "a")
    result = ""
    for pos in posTagUnStemmedwords:
        result += pos.__str__() + "\n"
#        if not pos[0]==pos[1]:
#            print pos
#            if( askCorrect() ):
#                posCorrectUnStemmedwords += 1
    text_file.write(result)
    text_file.close()

    #print posTagUnStemmed
    # Conclusion: NER tagging should be done BEFORE lower casing since the result is very poor otherwise
    posTagUnStemmedWords = nltk.pos_tag(Words)
    print "NER Tagged UnStemmed words"
    print nltk.ne_chunk(posTagUnStemmedwords)
    text_file = open("nerTagUnStemmedWords.txt", "a")
    result = ""
    for chunk in nltk.ne_chunk(posTagUnStemmedWords):
        result += chunk.__str__() + "\n"
#        if not isinstance(chunk[0],str):
#            print chunk
#            if( askCorrect() ):
#                nerCorrectUnStemmedWords += 1
    text_file.write(result)
    text_file.close()
    print "NER Tagged UnStemmed Words"
    print nltk.ne_chunk(posTagUnStemmedwords)
    text_file = open("nerTagUnStemmedLCwords.txt", "a")
    result = ""
    for chunk in nltk.ne_chunk(posTagUnStemmedwords):
        result += chunk.__str__() + "\n"
#        if not isinstance(chunk[0],str):
#            print chunk
#            if( askCorrect() ):
#                nerCorrectUnStemmedwords += 1
    text_file.write(result)
    text_file.close()
    stemmedWords = [porter.stem(t) for t in Words]
    posTagStemmedWords = nltk.pos_tag(stemmedWords)
    print "NER Tagged Stemmed Words"
    print nltk.ne_chunk(posTagStemmedWords)
    text_file = open("nerTagStemmedWords.txt", "a")
    result = ""
    for chunk in nltk.ne_chunk(posTagStemmedWords):
        result += chunk.__str__() + "\n"
#        if not isinstance(chunk[0],str):
#            print chunk
#            if( askCorrect() ):
#                nerCorrectStemmedWords += 1
    text_file.write(result)
    text_file.close()
    print "NER Tagged Stemmed words"
    print nltk.ne_chunk(posTagStemmedwords)
    text_file = open("nerTagStemmedLCwords.txt", "a")
    result = ""
    for chunk in nltk.ne_chunk(posTagStemmedwords): 
        result += chunk.__str__() + "\n"
#        if not isinstance(chunk[0],str):
#            print chunk
#            if( askCorrect() ):
#                nerCorrectStemmedwords += 1
    text_file.write(result)
    text_file.close()
 

#result = "";
#result += "Correct POS Tagged on Stemmed Lowercase Words: {0}\n".format(posCorrectStemmedwords)
#result += "Correct POS Tagged on Unstemmed Lowercase Words: {0}\n".format(posCorrectUnStemmedwords)
#result += "Correct NER Tagged on Stemmed Lowercase Words: {0}\n".format(nerCorrectStemmedwords)
#result += "Correct NER Tagged on UnStemmed Lowercase Words: {0}\n".format(nerCorrectUnStemmedwords)
#result += "Correct NER Tagged on Stemmed Uppercase Words: {0}\n".format(nerCorrectStemmedWords)
#result += "Correct NER Tagged on UnStemmed Uppercase Words: {0}\n".format(nerCorrectUnStemmedWords)
#result += "Total Words: {0}".format(totWords)
#text_file = open("Results.txt", "w")
#text_file.write(result)
#text_file.close()

#print result


    