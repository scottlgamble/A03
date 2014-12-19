#!/usr/bin/python

import os
import urllib2
import sys
from A03_Support import GetResultsPages,GetResultsPages,ExportItemsToCSV,getURLSuf,removeDuplicateStories,creatExportList, StatsFromIDURL
from Py_Tools2 import saveDict,readDict,getClipboardData,setClipboardData


if True:
    file_location = '/Users/scottgamble/Downloads/'
    os.chdir(file_location)

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
            
    Kudos       = ""
    Tags        = ""
    Raiting     = ""
    searchText  = ""
    author      = ""
    url_suf     = ""
    NumPages    = 1
    WordNum     = ""
    ships       = []
    larry       = {'fandom': "One Direction (Band)",'Rel':"Harry+Styles%2FLouis+Tomlinson"}
    stereck     = {'fandom': "Teen Wolf (TV)",'Rel':"Derek+Hale%2FStiles+Stilinski"}
    zaim        = {'fandom': "One Direction (Band)",'Rel':"Zayn+Malik%2FLiam+Payne"}
    ziall       = {'fandom': "One Direction (Band)",'Rel':"Niall+Horan%2FZayn+Malik"}
    naim        = {'fandom': "One Direction (Band)",'Rel':"Niall+Horan%2FLiam+Payne"}
    ships = [larry, stereck,zaim,ziall,naim]
    Method = ['search']
    
    
wordNum     = ">15000"
# wordNum   = ["12850","33920","5392","20331"]
# wordNum   =["74131"]
NumPages    = 30
SortBy      = ["revised_at","kudos_count","hits","bookmarks_count","comments_count"]
SortCol     = 1
# Kudos       = ">500"
# Tags        = ""
# searchText  = ""
# Raiting = "13" #13 explict
# author = ""
# ships = [larry, stereck]
# ships = [zaim,ziall,naim]
# ships = [stereck]
# ships = [""]
# Method = ['url']

ItemList = []
## Single Page
if 'search' in Method:
    checkChars = ['<','>','-']
    if len([x for x in checkChars if x in '_'.join(wordNum)])==0:
        NumPages = 1
        print('OnePage')
    else:
        #takes single wordNum and creates a list of 1 for loop
        wordNum = [wordNum]
## Standard Search
    for ship in ships:
        for wordNum_item in wordNum:
            try:
                url_suf = getURLSuf(ship,Tags,Kudos,searchText,Raiting,SortBy[SortCol], wordNum_item)
                ItemList.extend(GetResultsPages(url_suf,NumPages,ship))
            except:
                break

## By URL
if 'url' in Method:
    with open("/Users/scottgamble/PycharmProjects/Scripts/URLs.txt") as f:
        urls = [word.strip() for word in f]
    
    for url in urls:
            ItemList.extend(StatsFromIDURL(url))


# ['readCount', 'lastRead', 'chapters', 'fandom', 'storyURL', 'authorURL', 'words', 'bookmarks', 'relationships',
 # 'kudos', 'title', 'comments', 'summary', 'authorName','tags','seriesName','seriesNumber',]
 

fields = ['ID','title','lastRead','readCount','mynotes','fandom','summary','relationships','words','storyURL','kudos','hits']

# fields.extend(['seriesName','seriesNumber'])
# fields.extend(['tags'])

ItemList = removeDuplicateStories(ItemList)
ExportList = creatExportList(ItemList,fields)
ExportItemsToCSV(ExportList, '/Users/scottgamble/Downloads/')

    #
    # if OpenFinder == 1:
    #     subprocess.open(['open',file_location])
