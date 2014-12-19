import os
import urllib2
import sys
from A03_Support import GetResultsPages,GetResultsPages,ExportItemsToCSV,getURLSuf,removeDuplicateStories,creatExportList, StatsFromIDURL
from Py_Tools2 import saveDict,readDict,getClipboardData,setClipboardData


try:

except:
    pass


StatsFromIDURL(urls)

# ['readCount', 'lastRead', 'chapters', 'fandom', 'storyURL', 'authorURL', 'words', 'bookmarks', 'relationships',
 # 'kudos', 'title', 'comments', 'summary', 'authorName','tags','seriesName','seriesNumber',]
 

fields = ['ID','title','lastRead','readCount','mynotes','fandom','summary','relationships','words','storyURL','kudos','hits']

# fields.extend(['seriesName','seriesNumber'])
# fields.extend(['tags'])

