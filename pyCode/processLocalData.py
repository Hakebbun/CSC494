# Useage: bash processLocalData arg

# performs preprocessing on datafile for topic specified by arg

import sys
import urllib2
import nltk
import re
import spell as spellcheck
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


print("writing...")

# List of data files to be processed
trainDataFiles = ["depression-683", "eating-disorders-862", "sleep-problems-2099", "bipolar-affective-disorder-271", "25-Depression-Dysthymia-Seasonal-Affective-DisorderTest", "26-Bipolar-Disorder-CyclothymiaTest", "59-Sleep-Dreams-InsomniaTest", "75-Eating-DisordersTest"]

topic = trainDataFiles[int(sys.argv[1])]

fSource = open(topic + 'RAW' + '.txt','r')
fTarget = open(topic + '.txt','w')
stops = set(stopwords.words("english"))

# Iterate through each post in the file (each post is one line)
for post in fSource.readlines():

    # removing some punctuation
    post = re.sub('[!@#$.,?"--]', '', post)
    post = re.sub('[/]', ' ', post)

    #removing some common patterns
    post = re.sub("\quot", '', post)
    post = re.sub("<a(.*?)</a>", '', post)
    post = re.sub( '\s+', ' ', post ).strip()
    post = post.lower()
    words = post.split()

    # remove stop words
    words = [w for w in words if not w in stops]

    # run spell check on each word
    for i in range(0, len(words)):
        words[i] = spellcheck.correction(words[i])

    words = ' '.join(words)

    # Protect against anything crazy happening. Otherwise, just write to file
    try:
        fTarget.write(words + '\n')
    except UnicodeEncodeError as e:
        print("Unexpected characters! Skipping!")
        print(e)

# Cleanup
fSource.close()
fTarget.close()
print("Done!")
