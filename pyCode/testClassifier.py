# Tests the classifier. Can only be run after buildClassifier.py

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
from sklearn import decomposition

# Categories and files to read from
CATEGORIES = ["depression","bipolar-affective-disorder", "eating-disorders", "sleep-problems"]
TEST_FILES = ["25-Depression-Dysthymia-Seasonal-Affective-DisorderTest.txt", "26-Bipolar-Disorder-CyclothymiaTest.txt", "75-Eating-DisordersTest.txt","59-Sleep-Dreams-InsomniaTest.txt",]
CERTAINTY_MIN = float(sys.argv[1])

# Load the variables used for training
pickleIn = open('classifier.pkl', 'rb')
classifier = pickle.load(pickleIn)

pickleIn2 = open('vectorizer.pkl', 'rb')
vectorizer = pickle.load(pickleIn2)

pickleIn3 = open('tfTransformer.pkl', 'rb')
tf_transformer = pickle.load(pickleIn3)

pickleIn4 = open('sentimentDict.pkl', 'rb')
sentimentDict = pickle.load(pickleIn4)

testDataRAW = open('testDataManual.txt', 'r')

testData = []
expected = []
ANEW = []

# Iterate over the test files
for i in range(0, len(TEST_FILES)):
    curFile = open(TEST_FILES[i], "r")

    for text in curFile.readlines():
        expected.append(i)

        # tokenize
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

                # Uncomment BELOW FOR MEAN ANEW
                valence += float(sentimentDict[word][0])
                arousal += float(sentimentDict[word][3])
                dominance += float(sentimentDict[word][6])

        if(words != 0):
            valence = valence/words
            arousal = arousal/words
            dominance = dominance/words
            ANEW.append([valence, arousal, dominance])
        else:
            ANEW.append([0,0,0])

        fdist = " ".join(fdist)
        testData.append(fdist)

    curFile.close()

# Text processing complete, build BoW
train_data_features = vectorizer.transform(testData)
train_data_features = train_data_features.toarray()
train_data_features = np.append(train_data_features, ANEW, axis=1)

predictedprobs = classifier.predict_proba(train_data_features)
predicted = classifier.predict(train_data_features)

# read through the predictions to gather some data
success = 0
failure = 0

lowProbs = []

result = []
curClass = int(expected[0])

# placeholder array of [correct predictions for this class, total predictions for this class]
curResult = [0,0]

# placeholder array of distributions of predictions
distribution = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]

# iterate over predictions
for i in range(0, len(predicted)):

    # Check if we've changed classes (since test data is sorted)
    if(curClass != int(expected[i])):
        curClass = int(expected[i])
        result.append(curResult)
        curResult = [0,0]

    # check if this prediction is past our certainty threshold
    if(max(predictedprobs[i]) > CERTAINTY_MIN):
        curResult[1] = curResult[1] + 1
        if(int(expected[i]) == int(predicted[i].item())):
            success = success + 1
            curResult[0] = curResult[0] + 1
        else:
            failure = failure + 1

        # Increedment distribution for prediction
        distribution[curClass][int(predicted[i].item())] = distribution[curClass][int(predicted[i].item())] +1

    else:
        # If not certain enough, add to low-prob predictions
        lowProbs.append(max(predictedprobs[i]))

result.append(curResult)

# print out results
print("success: " + str(success))
print("total: " + str(success + failure))
print(distribution)
print(result)

print("Low probs: ")
# print(lowProbs)
print(len(lowProbs))
