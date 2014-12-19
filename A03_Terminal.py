#!/usr/bin/env python

import os
import sys
import subprocess




from A03_Support import GetResultsPages,GetResultsPages,ExportItemsToCSV,getURLSuf,removeDuplicateStories,GetNumPages,creatExportList
from Py_Tools2 import saveDict,readDict,getClipboardData,setClipboardData

file_location = '/Users/scottgamble/Downloads/'
NumPages_Default = 15
#
# full_url = getClipboardData
# print full_url[1]

if len(sys.argv)>0:
    full_url = sys.argv[1]

    url_suf = "&"+full_url.split("&", 1)[1]
    
    if True:
        ships = [{'fandom': "One Direction (Band)",'Rel':"Harry+Styles%2FLouis+Tomlinson"},{'fandom': "Teen Wolf (TV)",'Rel':"Derek+Hale%2FStiles+Stilinski"}]
        ItemList = []

    if (url_suf.find("Wolf"))>=0:
        ship = ships[1]
    elif (url_suf.find("Direction"))>=0:
        ship = ships[0]

    try:
        if len(sys.argv) >3:
            NumPages = int(sys.argv[2])
            print(sys.argv)
        else:
            NumPages = NumPages_Default
    except:
        NumPages = NumPages_Default       
        
    print chr(27) + "[2J"
    # print(str(NumPages) + " Pages")
    print("Retreiving Items")
    ItemList.extend(GetResultsPages(url_suf,NumPages,ship))
    print("Removing Duplicates")
    ItemList = removeDuplicateStories(ItemList)
    print("Exporting")
    # ['readCount', 'lastRead', 'chapters', 'fandom', 'storyURL', 'authorURL', 'words', 'bookmarks', 'relationships', 'kudos', 'title', 'comments', 'summary', 'authorName','tags']
    fields = ['ID','title','lastRead','readCount','mynotes','fandom','summary','relationships','words','storyURL','kudos','tags','hits','bookmarks']

    ExportList = creatExportList(ItemList,fields)
    ExportItemsToCSV(ExportList, '/Users/scottgamble/Downloads/')
    # setClipboardData(ExportList)
    
    subprocess.Popen(['open',file_location])   
    
else:
    print("URL Not Properly Formated")

