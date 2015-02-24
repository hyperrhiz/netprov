# -*- coding: utf-8 -*-
# thanks to Simon Hudson for a substantial portion of this script. http://hudsonsoapbox.com/2013/06/09/extracting-historical-data-from-twitter-using-python/
# for use with searches by username, not hashtag
import csv, sys
from bs4 import BeautifulSoup

def worker(stem="netprov"): # this section makes it so you can run the script with command "python netprov.py <filename>"
    ins=stem + ".html"
    outs=stem + ".csv"
    f = csv.writer(open(outs, "w"), delimiter = ",") # csv output file, changed delimiter to comma
    f.writerow(["Username", "Time and Date", "Tweet Text", "URL Links", "Twitter Permalink"]) # csv column headings
    soup = BeautifulSoup(open(ins)) #input html document 
  
    prestrip = soup.find_all("li", "js-stream-item stream-item stream-item expanding-stream-item cards-forward ") # find every li with this style
    for strip in prestrip: # strip out cards-forward style because it's not in all instances
        strip['class'] = "js-stream-item stream-item stream-item expanding-stream-item " # that trailing space is because of a weird newline issue with the browser

    litop = soup.find_all("li", "js-stream-item stream-item stream-item expanding-stream-item ") # all the tasty stuff is inside li tags with this style

    for li in litop:
        try:
            username = li.find("span", "username js-action-profile-name").get_text()
        except:
            username = " "
            print "No username"
        try:
            timedate = li.find("a", "tweet-timestamp js-permalink js-nav js-tooltip").attrs["title"] # date and time. See below.
        except:
            try:
                timedate = li.find("a", "tweet-timestamp js-permalink js-nav js-tooltip").attrs["data-original-title"] # sometimes "title" is named "data-original-title". This catches it.
            except:
                timedate=" "
                print "No timestamp"
        try:
            tweettext = li.find("p", "js-tweet-text tweet-text").get_text().encode("utf-8").replace("\n","") #Tasty tweet text
        except:
            tweettext = " "
            print "No tweet text"
        try:
            URLlinked = li.find("a", "twitter-timeline-link").attrs["href"] # URLs included in the tweet. Not always there
        except:
            URLlinked = " "
            print "No URL"
        try:
            permalink = li.find("a", "tweet-timestamp js-permalink js-nav js-tooltip").attrs["href"] # twitter permalink
        except:
            permalink=" "
            print "No permalink"

        f.writerow([username, timedate, tweettext, URLlinked, permalink]) # write it to the file
        
if __name__ == "__main__":
    worker(sys.argv[1])