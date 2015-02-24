# -*- coding: utf-8 -*-
# thanks to Simon Hudson for a substantial portion of this script. http://hudsonsoapbox.com/2013/06/09/extracting-historical-data-from-twitter-using-python/
#for use with searches by username, not hashtag
import csv, sys
from bs4 import BeautifulSoup

def worker(stem="netprov"): # this section makes it so you can run the script with command "python netprov.py <filename>"
    ins=stem + ".html"
    outs=stem + ".csv"
    f = csv.writer(open(outs, "w"), delimiter = ",") # csv output file, changed delimiter to comma
    f.writerow(["Username", "Time and Date", "Tweet Text", "URL Links"]) # csv column headings
    soup = BeautifulSoup(open(ins)) #input html document 
  
    divtop = soup.find_all("div", "StreamItem js-stream-item") # all the tasty stuff is inside div tags with this style

    for div in divtop:
        try:
            username = div.find("span", "ProfileTweet-screenname u-dir").get_text()
        except:
            username = " "
            print "No username"
        try:
            timedate = div.find("a", "ProfileTweet-timestamp js-permalink js-nav js-tooltip").attrs["title"] # date and time. See below.
        except:
            timedate=" "
            print "No timestamp"
        try:
            tweettext = div.find("p", "ProfileTweet-text js-tweet-text u-dir").get_text().encode("utf-8").replace("\n","") #Tasty tweet text
        except:
            tweettext = " "
            print "No tweet text"
        try:
            URLlinked = div.find("a", "twitter-timeline-link").attrs["href"] # URLs included in the tweet. Not always there
        except:
            URLlinked = " "
            print "No URL"

        f.writerow([username, timedate, tweettext, URLlinked]) # write it to the file
        
if __name__ == "__main__":
    worker(sys.argv[1])