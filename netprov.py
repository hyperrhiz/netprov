# -*- coding: utf-8 -*-
import csv, sys
from bs4 import BeautifulSoup

def worker(stem="netprov"):
    ins=stem + ".html"
    outs=stem + ".csv"
    f = csv.writer(open(outs, "w"), delimiter = ",") #csv output file, changing '/t' changed how the file is delimited. /t is by tab.
    f.writerow(["Username", "Time and Date", "Tweet Text", "URL Links", "Twitter Permalink"]) #csv column headings
    soup = BeautifulSoup(open(ins)) #input html document 
  
    prestrip = soup.find_all("li", "js-stream-item stream-item stream-item expanding-stream-item cards-forward ")
    for strip in prestrip:
        strip['class'] = "js-stream-item stream-item stream-item expanding-stream-item "

    litop = soup.find_all("li", "js-stream-item stream-item stream-item expanding-stream-item ")#print timestrip

    for li in litop:
        try:
            username = li.find("span", "username js-action-profile-name").get_text()
        except:
            username = " "
            print "No username"
        try:
            timedate = li.find("a", "tweet-timestamp js-permalink js-nav js-tooltip").attrs["title"]
        except:
            try:
                timedate = li.find("a", "tweet-timestamp js-permalink js-nav js-tooltip").attrs["data-original-title"]
            except:
                timedate=" "
                print "No timestamp"
        try:
            tweettext = li.find("p", "js-tweet-text tweet-text").get_text().encode("utf-8").replace("\n","")
        except:
            tweettext = " "
            print "No tweet text"
        try:
            URLlinked = li.find("a", "twitter-timeline-link").attrs["href"]
        except:
            URLlinked = " "
            print "No URL"
        try:
            permalink = li.find("a", "tweet-timestamp js-permalink js-nav js-tooltip").attrs["href"]
        except:
            permalink=" "
            print "No permalink"

        f.writerow([username, timedate, tweettext, URLlinked, permalink])
        
if __name__ == "__main__":
    worker(sys.argv[1])