# Usage: getDataPatientInfo arg1 arg2
# Gets arg2 pages of forum posts from patient.info related to topic arg1
# Also prints data related to the number of unique users

import sys
import urllib2
import nltk
import re
from bs4 import BeautifulSoup

print("writing...")
genU = "http://patient.info"

topic = sys.argv[1]
numPages = int(sys.argv[2])
userDict = {}

f = open(topic + 'RAW' + '.txt','w')
for p in range(0, numPages):
    print("on page: " + str(p))
    # open URL
    urlP1 = "http://patient.info/forums/discuss/browse/" + topic + "?page="
    pageNum = p
    urlP2 = "#group-discussions"
    url = urlP1 + str(pageNum) + urlP2
    data = urllib2.urlopen(url).read()

    # set up the soup
    soup = BeautifulSoup(data, "html.parser")
    posts = soup.find_all("a", class_="avatar-hover")

    for i in range(0, len(posts)):
        userDict[posts[i].get_text()] = True
        print(posts[i].get_text())
        # Grab the link to the actual post
        postLink = genU + posts[i].find("a")["href"]

        postData = urllib2.urlopen(postLink).read()

        postSoup = BeautifulSoup(postData,"html.parser")
        postBodySoup = postSoup.find("div", class_="post-content").find_all("p")
        postBody = ""
        for m in range(0, len(postBodySoup)):
            postBody += postBodySoup[m].get_text() + " "

        try:
            f.write(postBody.encode('utf-8') + '\n')
        except UnicodeEncodeError as e:
            print("Unexpected characters! Skipping!")
            print(e)
            print(postLink)

f.close()
print(topic)
print(len(userDict.keys()))
