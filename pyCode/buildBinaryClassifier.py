import sys
import urllib2
import nltk
import re
import pickle
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

trainDataFiles = ["depression-683.txt", "bipolar-affective-disorder-271.txt"]
CATEGORIES = ["depression", "bipolar-affective-disorder"]

KEYWORDS = ["bipolar"]
KEYWORD_WEIGHT = 5000;

data = []
dataCat = []

for i in range(0, len(trainDataFiles)-1):
    print("Opening new file")
    trainData = open(trainDataFiles[i], "r")
    for text in trainData:

        # tokenize
        fdist = nltk.FreqDist(nltk.tokenize.word_tokenize(str(text)))

        stops = set(stopwords.words("english"))

        # remove stopwords (TODO: Might be a better way of doing this)
        fdist = [w for w in fdist if not w in stops]

        # for KEY in KEYWORDS:
        #     if KEY in fdist:
        #         print("Found key: " + KEY + " adding weight...")
        #         for weight in range(0,KEYWORD_WEIGHT):
        #             fdist.append(KEY)

        fdist = " ".join(fdist)

        data.append(fdist)
        dataCat.append(i)

# Text processing complete, build BoW
vectorizer = CountVectorizer(analyzer = "word",
                             tokenizer = None,
                             preprocessor = None,
                             stop_words = None,
                             max_features = 5000)
train_data_features = vectorizer.fit_transform(data)

print(train_data_features.shape)

tf_transformer = TfidfTransformer(use_idf=False).fit(train_data_features)
train_data_counts = tf_transformer.transform(train_data_features)

print(train_data_counts.shape)

clf = MultinomialNB().fit(train_data_counts, dataCat)

# make a pickle object to save the classifier in
pickleOut = open('BinClassifier.pkl', 'wb')
pickleOut2 = open('BinVectorizer.pkl', 'wb')
pickle.dump(clf, pickleOut, pickle.HIGHEST_PROTOCOL)
pickle.dump(vectorizer, pickleOut2, pickle.HIGHEST_PROTOCOL)
