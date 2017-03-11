#Assignment 1 Part 1 using NLTK
#By Kamidi Preetham, 130101031 
#Group: ANTIntelligence

import nltk
from nltk.corpus import brown
from nltk.util import ngrams
setnences = list(brown.sents())    #Sentences
total_words = brown.words()
dict_words = list(set(total_words))    #Dictionary of words
bigrams = ngrams(total_words, 2)
trigrams = ngrams(total_words, 3)
unifreq = nltk.FreqDist(total_words)
bifreq = nltk.FreqDist(bigrams)
trifreq = nltk.FreqDist(trigrams)
unifreq.plot(30,cumulative=False)   #Plots for Unigrams, Bigrams and Trigrams
bifreq.plot(30,cumulative=False)
trifreq.plot(30,cumulative=False)