#!/usr/bin/python
import subprocess
import re
import urllib2
import time
from bs4 import BeautifulSoup
import csv
import sys
import os
# url = "file:///Users/scottgamble/1D All/Code/example1.html"
# soup = BeautifulSoup(url)
file_location = '/Users/scottgamble/Downloads/'
os.chdir(file_location)

#From Command Line



wordNum = ">45000"
NumPages  = 7
SortBy    = ["revised_at","kudos_count","hits","bookmarks_count"]
SortCol   = 1
Kudos     = ""
Tags = ""
Raiting = ""
searchText = ""
# Tags = "BDSM"
# Raiting = "13" #13 explict


fandom = "One Direction (Band)"
Rel = "Harry+Styles%2FLouis+Tomlinson"

fandom = "Teen Wolf (TV)"
Rel = "Derek+Hale%2FStiles+Stilinski"

OpenFinder = 1
if len(sys.argv) > 1:
    NumPages = 1
    OpenFinder = 0
    SortCol = 0

if len(sys.argv) == 2:
    wordNum = sys.argv[1]
    # print wordNum

elif len(sys.argv) == 3:
    wordNum = sys.argv[2]
    if sys.argv[1][0].upper() == "T":
        fandom = "Teen Wolf (TV)"
        Rel = "Derek+Hale%2FStiles+Stilinski"
    elif sys.argv[1][0] == "1":
        fandom = "One Direction (Band)"
        Rel = "Harry+Styles%2FLouis+Tomlinson"



url_pre = "http://archiveofourown.org/works/search?commit=Search&page="
url_suf = "&work_search%5Bbookmarks_count%5D=&work_search%5Bcharacter_names%5D=&work_search%5B"\
            "comments_count%5D=&work_search%5Bcomplete%5D=1&work_search%5Bcreator%5D=&work_search%5B"\
            "fandom_names%5D=" + urllib2.quote(fandom) + "&work_search%5B"\
            "freeform_names%5D="+urllib2.quote(Tags)+ "&work_search%5Bhits%5D=&work_search%5B"\
            "kudos_count%5D=" + urllib2.quote(Kudos) + "&work_search%5Blanguage_id%5D=1&"\
            "work_search%5Bquery%5D="+ urllib2.quote(searchText) +"&work_search%5B"\
            "rating_ids%5D="+ urllib2.quote(Raiting) +"&work_search%"\
            "5Brelationship_names%5D=" + Rel + "&work_search%5Brevised_at%5D=&work_search%5Bshow_restricted%5D=false&work_search%5Bsingle_chapter%5D=0&work_search%5B"\
            "sort_column%5D=" + SortBy[SortCol] + "&work_search%5Bsort_direction%5D=&work_search%5Btitle%5D=&work_search%5B" \
            "word_count%5D=" + urllib2.quote(wordNum)


            
time_txt = time.strftime("%Y%m%d-%H_%M_%S")
with open("Stories_" + time_txt + ".csv", "wb") as f:
    writer = csv.writer(f)
    headers = [['Title Name',"","","","Fandom",'summary','relationships','words','link']]
    writer.writerows(headers)
    for page in range(1,NumPages+1):
        url = url_pre+str(page)+url_suf
        # print(url)
        # url = 'file:///Users/scottgamble/PycharmProjects/Scripts/Page1.html'
        
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page)



        articlesList = soup.find_all('li', 'work blurb group')


        for article in articlesList:

            title       = article.div.h4.find_all('a')
            title_link  = title[0].attrs
            title_link  = 'http://archiveofourown.org/'+str(title_link[u'href'])
            # print title[0].contents
            title_name  =title[0].contents[0].encode("ascii", "ignore")
            # print title_name
            try:
                author_link = title[1].attrs
                author_link = 'http://archiveofourown.org/'+str(author_link[u'href'])
                author_name = str(title[1].string)
            except:
                author_link = "None"
                author_link = "None"
            try:
                summary = str(article.blockquote.get_text().encode("punycode"))
                summary = summary.replace("\"", "'").strip()
                # print summary
                summary = re.sub("\n\-.*$","",summary)
                # print summary
            except:
                summary = "None Given"
            relation = article.findAll('li','relationships')
            relation_txt = ""
            for r in range(0,len(relation)):
                relation_txt = relation_txt + relation[r].a.string + "\n"
            relation_txt = relation_txt.strip()
            # print article.prettify()
            stats       = article.dl.find_all(['dd','dt'])

            words       = str(stats[1].contents[0])
            chapters    = str(stats[3].contents[0])
            comments = 0
            kudos = 0
            bookmarks = 0
            hits = 0
            for x in range(0, len(stats)):
                stat_type   = str(stats[x].contents[0]).strip()
                if stat_type == "Comments:":
                    comments = str(stats[x+1].a.contents[0]).strip()
                elif stat_type == "Kudos:":
                    kudos = str(stats[x+1].a.contents[0]).strip()
                elif stat_type == "Bookmarks:":
                    bookmarks = str(stats[x+1].a.contents[0]).strip()
                elif stat_type == "Hits:":
                   hits = str(stats[x+1].contents[0]).strip()
                elif stat_type == "Words:":
                      words = str(stats[x+1].contents[0]).strip()
                elif stat_type == "Chapters:":
                    chapters = str(stats[x+1].contents[0]).strip()
            # # [['Title','link','summary','chapters','comments','kudos','hits']]
            # temp = [[title_name,title_link,[summary],[relation_txt],chapters,comments,kudos,hits,bookmarks,author_name,author_link]]
            # print summary.strip()
            # [['Title Name','summary','relationships','words','link']]
            writer.writerows([[title_name,"","",kudos,fandom,summary,relation_txt,words,title_link]])
        # time.sleep(1)  
    if OpenFinder == 1:
        subprocess.Popen(['open',file_location])    
