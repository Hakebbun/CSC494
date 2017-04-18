# Usage: bash buildClassifier arg
# Builds a classifier with max features == arg and saves in it classifier.pkl
# Requires a sentimentDict.pkl To build one, run buildSentimentDict


import sys
import urllib2
import nltk
import re
import pickle
import numpy as np
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn import decomposition

# list of data files to train classifier from, and a list of classes
trainDataFiles = ["depression-683.txt", "bipolar-affective-disorder-271.txt",  "eating-disorders-862.txt", "sleep-problems-2099.txt"]
CATEGORIES = [ "depression","bipolar-affective-disorder", "eating-disorders", "sleep-problems"]

MAX_FEATURES = int(sys.argv[1])

pickleIn = open('sentimentDict.pkl', 'rb')
sentimentDict = pickle.load(pickleIn)

data = []
dataCat = []
ANEW = []

# Iterate over each data file
for i in range(0, len(trainDataFiles)):
    print("Opening new file")
    trainData = open(trainDataFiles[i], "r")
    for text in trainData:

        # tokenize and remove stopwords
        fdist = nltk.FreqDist(nltk.tokenize.word_tokenize(str(text)))

        # get ANEW features and store them elsewhere
        valence = 0
        arousal = 0
        dominance = 0
        words = 0
        for word in fdist:
            if(word in sentimentDict):
                words += 1

                # Uncomment BELOW for HISTOGRAM ANEW
                # if(float(sentimentDict[word][0]) < 5):
                #     valence += 1
                # if(float(sentimentDict[word][3]) < 5):
                #     arousal += 1
                # if(float(sentimentDict[word][6]) < 5):
                #     dominance += 1

                # Uncomment BELOW for MEAN ANEW
                valence += float(sentimentDict[word][0])
                arousal += float(sentimentDict[word][3])
                dominance += float(sentimentDict[word][6])

        # protect from dividing by 0
        if(words != 0):
            valence = valence/words
            arousal = arousal/words
            dominance = dominance/words
            ANEW.append([valence, arousal, dominance])
        else:
            ANEW.append([0,0,0])

        # stitch the words back, add this vector the matrix, add a class to this vector
        fdist = " ".join(fdist)
        data.append(fdist)
        dataCat.append(i)

# Build the vectorizer
vectorizer = CountVectorizer(analyzer = "word",
                             tokenizer = None,
                             preprocessor = None,
                             stop_words = None,
                             binary = False,
                             max_features = MAX_FEATURES)
train_data_features = vectorizer.fit_transform(data)
train_data_features = train_data_features.toarray()
train_data_features = np.append(train_data_features, ANEW, axis=1)

# Fit the classifier to the training data along with the labels
clf = MultinomialNB().fit(train_data_features, dataCat)

# Save all of our objects so we can use them in the testing script
pickleOut = open('classifier.pkl', 'wb')
pickleOut2 = open('vectorizer.pkl', 'wb')
pickleOut3 = open('tfTransformer.pkl', 'wb')
pickle.dump(clf, pickleOut, pickle.HIGHEST_PROTOCOL)
pickle.dump(vectorizer, pickleOut2, pickle.HIGHEST_PROTOCOL)
pickle.dump(tf_transformer, pickleOut3, pickle.HIGHEST_PROTOCOL)
