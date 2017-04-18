# Builds a sentiment dictionary of: word -> [valence, arousal, dominance]
# and saves it in sentimentDict.pkl

import csv
import sys
import urllib2
import nltk
import re
import pickle
import numpy as np

csvDIR = 'Ratings_Warriner_et_al.csv'
sentimentDict = {}

with open(csvDIR, 'rb') as csvFile:
    csvReader = csv.reader(csvFile, delimiter='\n', quotechar='|')
    for row in csvReader:
        rowData = row[0].split(',')
        sentimentDict[rowData[1]] = rowData[2:]

pickleOut = open('sentimentDict.pkl', 'wb')
pickle.dump(sentimentDict, pickleOut, pickle.HIGHEST_PROTOCOL)
