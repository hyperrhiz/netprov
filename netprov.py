# -*- coding: utf-8 -*-
# thanks to Simon Halfdan at http://pastebin.com/10fSBZZB for most of this script. You rock, simon

import csv
from bs4 import BeautifulSoup

f = csv.writer(open("./sootfall.csv", "w"), delimiter = ",") # csv output file, changed to comma delimiter
f.writerow(["Username", "Time and Date", "Tweet Text", "URL Links", "Twitter Permalink"]) # csv column headings

soup = BeautifulSoup(open("./sootfall.html")) #input html document 
prestrip = soup.find_all("li", "js-stream-item stream-item stream-item expanding-stream-item cards-forward ") # gotta get rid of that cards-forward style
for strip in prestrip:
    strip['class'] = "js-stream-item stream-item stream-item expanding-stream-item "

litop = soup.find_all("li", "js-stream-item stream-item stream-item expanding-stream-item ") # still has annoying space from bad line endings. what you gonna do

for li in litop:
    try:
        username = li.find("span", "username js-action-profile-name").get_text() # twitter username
    except: # these excepts are all just-in-cases for empty returns
        username = " "
        print "No username"
    try:
        timedate = li.find("a", "tweet-timestamp js-permalink js-nav js-tooltip").attrs["title"] # date and time of tweet
    except:
        try:
            timedate = li.find("a", "tweet-timestamp js-permalink js-nav js-tooltip").attrs["data-original-title"] # some of these have a different named attribute
        except:
            timedate=" "
            print "No timestamp"
    try:
        tweettext = li.find("p", "js-tweet-text tweet-text").get_text().encode("utf-8").replace("\n","") # the magical tweet text
    except:
        tweettext = " "
        print "No tweet text"
    try:
        URLlinked = li.find("a", "twitter-timeline-link").attrs["href"] # for when there's a URL. not always the case
    except:
        URLlinked = " "
        print "No URL"
    try:
        permalink = li.find("a", "tweet-timestamp js-permalink js-nav js-tooltip").attrs["href"] #permalink to tweet
    except:
        permalink=" "
        print "No permalink"

    f.writerow([username, timedate, tweettext, URLlinked, permalink]) #write it to the csv file