# Usage: getTestData arg1 arg2
# Gets arg2 pages of forum posts from psychlinks related to topic arg1
# Also prints data related to the number of unique users

import sys
import urllib2
import nltk
import re
from bs4 import BeautifulSoup

print("writing...")

genU = "https://forum.psychlinks.ca/forumdisplay.php?"
genU2 = "https://forum.psychlinks.ca/"
topic = sys.argv[1]
numPages = int(sys.argv[2])

userDict = {}

f = open(topic + 'TestRAW' + '.txt','w')
for p in range(0, numPages):
    print("on page: " + str(p))
    # open URL
    urlP1 = genU + topic
    pageNum = p
    urlP2 = "/page"
    url = urlP1 + urlP2 + str(pageNum)
    data = urllib2.urlopen(url).read()

    # set up the soup
    soup = BeautifulSoup(data, "html.parser")
    threadOl = soup.find("ol", class_="threads")
    posts = threadOl.find_all("li", class_="threadbit")

    for i in range(1, len(posts)):
        userDict[posts[i].find("a", class_="username").get_text()] = True
        # Grab the link to the actual post
        postLink = genU2 + posts[i].find("a", class_="title")["href"]

        postLink = re.sub('&s=(.*)','',postLink)
        postData = urllib2.urlopen(postLink).read()

        postSoup = BeautifulSoup(postData,"html.parser")
        postBodySoup = postSoup.find("div", class_="content").find("blockquote")
        for m in range(0, len(postBodySoup)):
            bodyText = re.sub('(\s+)', ' ', postBodySoup.get_text())

        try:
            f.write(bodyText.encode('utf-8') + '\n')
        except UnicodeEncodeError as e:
            print("Unexpected characters! Skipping!")
            print(e)
            print(postLink)

f.close()

print(topic)
print(len(userDict.keys()))
