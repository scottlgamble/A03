#!/usr/bin/python

from bs4 import BeautifulSoup
import re
import urllib2
import time
import csv
import math
import subprocess
import sys
test = 0
if __name__ == '__main__':
    print ('Test Mode')
    test = 1

def GetResultsPages(url_suf,NumPages,ship):
    url_pre = "http://archiveofourown.org/works/search?commit=Search&page="
    MultiPageItemList = []
    if NumPages != 1:
        NumPage_Lookup = GetNumPages(url_pre+str(1)+url_suf)
        if NumPage_Lookup < NumPages:
            NumPages = NumPage_Lookup
    if NumPages == 0:
        NumPages = 1
    if test == 0:
        print("Number of Pages" + str(NumPages))
    
    for page in range(NumPages):
       
        url = url_pre+str(page+1)+url_suf
        # print url
        SinglePageItemList = ArticlesFromSingleURL(url,ship)
        try:
            MultiPageItemList.extend(SinglePageItemList)
        except:
            break
    return MultiPageItemList


def ArticlesFromSingleURL(url,ship):
    storyItemsList = []
    if test == 1:
        url = 'file:///Users/scottgamble/PycharmProjects/Scripts/Page1.html'
    # print(url)
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    storiesList = soup.find_all('li', 'work blurb group')
    # print(len(storiesList))
    for story in storiesList:
        title_block       = story.div.h4.find_all('a')
        storyURL  = title_block[0].attrs
        storyURL  = 'http://archiveofourown.org/'+str(storyURL[u'href'])

        fandom = str(story.div.h5.a.get_text().encode("ascii", "ignore"))
        if (fandom.find("Wolf"))>=0:
            fandom = "Teen Wolf (TV)"
        elif (fandom.find("Direction"))>=0:
           fandom = "One Direction (Band)"
        # print fandom
        # print title[0].contents
        title  =title_block[0].contents[0].encode("ascii", "ignore")
        # print title_name

        try:
            authorURL = title_block[1].attrs
            authorURL = 'http://archiveofourown.org/'+str(authorURL[u'href'])
            authorName = str(title_block[1].string)
        except:
            authorURL = "None"
            authorName= "None"
        try:
            summary = str(story.blockquote.get_text().encode("punycode"))
            summary = summary.replace("\"", "'").strip()
            # print summary
            summary = re.sub("\n\-.*$","",summary)
            # print summary
        except:
            summary = "None Given"

        relation_txt = ""
        relationshipSoup = story.findAll('li','relationships')
        for index,relationship in enumerate(relationshipSoup):
            relation_txt = relation_txt + relationshipSoup[index].a.string + "\n"
        relation_txt = relation_txt.strip()


        tagTxt=""
        tagList = story.findAll('li','freeforms')
        for index,tag in enumerate(tagList):
            tagTxt = tagTxt + tagList[index].a.string + "\n"
        tagTxt = tagTxt.strip()
        try:
            seriesList      = story.findAll('ul','series')
            seriesNumber    = str(seriesList[0].li.strong.contents).encode("ascii", "ignore").strip() 
            seriesName      = str(seriesList[0].li.a.contents).encode("ascii", "ignore").strip() 
        except:
            seriesNumber    = ""
            seriesName      = ""
        stats       = story.dl.find_all(['dd','dt'])

        words       = str(stats[1].contents[0])
        chapters    = str(stats[3].contents[0])
        comments = 0
        kudos = 0
        bookmarks = 0
        hits = 0
        # print(stats)
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

        
        storyID = re.search('works/(\d+)',storyURL).group(1)
        
        storyItems =   { \
            'title':title, \
            'storyURL':storyURL, \
            'authorURL':authorURL, \
            'authorName':authorName, \
            'summary':summary, \
            'kudos':kudos, \
            'bookmarks':bookmarks,
            'words':words, \
            'chapters':chapters, \
            'comments':comments, \
            'relationships':relation_txt,\
            'fandom':fandom,\
            'hits':hits,\
            'ID': storyID,\
            'tags':tagTxt,\
            'seriesName':seriesName,\
            'seriesNumber':seriesNumber\
            }
        storyItemsList.append(storyItems)
    return storyItemsList

def ExportItemsToCSV(ExportList,fileLocation):
    if test == 1:
        print("No Export Test Mode")
        return
    FileExportName =    "Stories_" + time.strftime("%Y.%m.%d-%H_%M_%S") + ".csv"
    #My Notes	Fandom	Summary	Relationships	Words	Link
    FileExportName = fileLocation+FileExportName
    with open(FileExportName, "wb") as f:
        writer = csv.writer(f)
        for row in ExportList:
            # print row
            try:
                writer.writerows([row])
            except:
                continue


def creatExportList(ItemList,fields):
    # FileExportName =    "Stories_" + time.strftime("%Y.%m.%d-%H_%M_%S") + ".csv"
    if len(fields)==0:
        fields = ['ID','title','lastRead','readCount','mynotes','fandom','summary','relationships','words','storyURL','kudos','hits']
    if len(ItemList)==0:
        # print("Empty List")
        sys.exit()
    HeaderDict =   {'title':'Title Name', \
        'storyURL':'Link', \
        'authorURL':'Author Link', \
        'authorName':'Author Name', \
        'summary':'Summary', \
        'kudos':'kudos', \
        'bookmarks':'bookmarks',\
        'words':'words', \
        'chapters':'chapters', \
        'comments':'comments', \
        'fandom':'Fandom',\
        'relationships':'relationships',\
        'lastRead':'Last Read',\
        'readCount':'Read Count',\
        'hits':'Hits',\
        'mynotes':"My Notes",\
        'ID':"Story ID",\
        'tags':'Tags',\
        'seriesName':'Series Name',\
        'seriesNumber':'Number In Series',\
        'PubDate': 'Publication Date',\
        'CompletedDate:': 'Completed Date'\
        }

    #My Notes	Fandom	Summary	Relationships	Words	Link
    ItemList.insert(0,HeaderDict)
    ExportList = []
    for story in ItemList:
        # writer.writerows()
        row = []
        for field in fields:
            if field =="":
                row.append("")
            else:
                try:
                    data = story.get(field).encode('ascii','ignore')
                except:
                    data = story.get(field)
                row.append(data)

        try:
            ExportList.extend([row])
        except:
            continue
    return ExportList


def getURLSuf(ship,Tags,Kudos,searchText,Raiting,SortByValue, wordNum):
    try:
        fandom = ship.get('fandom')
    except:
        fandom = ""
    try:
        Rel = ship.get('Rel')
    except:
        Rel = ""

    url_suf = "&work_search%5Bbookmarks_count%5D=&work_search%5Bcharacter_names%5D=&work_search%5B"\
            "comments_count%5D=&work_search%5Bcomplete%5D=1&work_search%5Bcreator%5D=&work_search%5B"\
            "fandom_names%5D=" + urllib2.quote(fandom) + "&work_search%5B"\
            "freeform_names%5D="+urllib2.quote(Tags)+ "&work_search%5Bhits%5D=&work_search%5B"\
            "kudos_count%5D=" + urllib2.quote(Kudos) + "&work_search%5Blanguage_id%5D=1&"\
            "work_search%5Bquery%5D="+ urllib2.quote(searchText) +"&work_search%5B"\
            "rating_ids%5D="+ urllib2.quote(Raiting) +"&work_search%"\
            "5Brelationship_names%5D=" + Rel + "&work_search%5Brevised_at%5D=&work_search%5Bshow_restricted%5D=false&work_search%5Bsingle_chapter%5D=0&work_search%5B"\
            "sort_column%5D=" + SortByValue + "&work_search%5Bsort_direction%5D=&work_search%5Btitle%5D=&work_search%5B" \
            "word_count%5D=" + urllib2.quote(wordNum)
    return url_suf
    
    
def removeDuplicateStories(StoryList):
    try:
        with open("/Users/scottgamble/PycharmProjects/Scripts/ExistingStories.txt") as f:
            ExistingStories = [word.strip() for word in f]
        seen.add(tuple(ExistingStories))
    except:
        pass
    seen = set()
    uniqueStoryList = []
    for d in StoryList:
        id 
        t = tuple(d.get('ID'))
        if t not in seen:
            seen.add(t)
            uniqueStoryList.append(d)
    return uniqueStoryList
    
def GetNumPages(url):
    if test == 1:
        return int(2)
    storiesPerPage = 20
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    found_row = soup.body.div.find(id="main").h3.contents[0].encode("ascii", "ignore").split(" ")[0]
    foundCount = int(found_row)
    NumPages = math.ceil(float(foundCount)/storiesPerPage)
    print "GetNumPages"
    return int(NumPages)

def StatsFromIDURL(url):
    
    if test == 1:
        url = 'file:///Users/scottgamble/PycharmProjects/Scripts/SingleStory.html'
        # page = urllib2.urlopen(url)
    else:
        url         = url + "?view_adult=true"
        # req         = urllib2.Request(url)
        # response    = urllib2.urlopen(url)
    print url
    page    = urllib2.urlopen(url)
    url2    = page.geturl()
    print url2
    # page2    = urllib2.urlopen(url2)
    # time.sleep(0.5)     
    r = requests.get(url2, timeout=5)
    soup = BeautifulSoup(r.text)
    # print soup.body.div.prettify()
    
    header  = soup.findAll('dl', {'class':'work meta group'})
    # header = story[0]
    print header

    relationshipSoup    = soup.findAll('dd',{'class': 'relationship tags'})[0]
    fandomSoup          = soup.findAll('dd',{'class': 'fandom tags'})[0]
    tagSoup             = header.findAll('dd',{'class': 'freeform tags'})[0]
    statSoup            = header.findAll('dd',{'class': 'stats'})[0]
    
    title_block         = soup.find(id='workskin').div
    
    storyURL  = url
    ##Title Block

    #title
    title = title_block.find_all('h2','title heading')
    title = "".join(title[0].contents[0]).strip()
    
    #Author
    try:
        authorURL = title_block.find_all('h3','byline heading')
        authorURL = authorURL[0].a.string
        authorURL = 'http://archiveofourown.org/'+str(authorURL[u'href'])
        authorName = str(title_block[1].string)
    except:
        authorURL = "None"
        authorName= "None"

    #Summary    
    try:
        summary = title_block.find_all('div','summary module')
        summary = str(summary.blockquote.get_text().encode("punycode"))
        summary = summary.replace("\"", "'").strip()
        # print summary
        summary = re.sub("\n\-.*$","",summary)
        # print summary
    except:
        summary = "None Given"


    #Fandom
    fandom = fandomSoup.find_all('li')
    fandom = fandom[0].a.string
    if (fandom.find("Wolf"))>=0:
        fandom = "Teen Wolf (TV)"
    elif (fandom.find("Direction"))>=0:
       fandom = "One Direction (Band)"
       
    #Relationships
    relation_txt = ""
    relationshipSoup_List = relationshipSoup.find_all('li')
    
    for index,relationship in enumerate(relationshipSoup_List):
        relation_txt = relation_txt + relationshipSoup_List[index].a.string + "\n"
    relation_txt = relation_txt.strip()

    #Tags
    tagTxt=""
    tagList = tagSoup.find_all('li')
    
    for index,tag in enumerate(tagList):
        tagTxt = tagTxt + tagList[index].a.string + "\n"
    tagTxt = tagTxt.strip()
    
    try:
        seriesList      = story.findAll('ul','series')
        seriesNumber    = str(seriesList[0].li.strong.contents).encode("ascii", "ignore").strip() 
        seriesName      = str(seriesList[0].li.a.contents).encode("ascii", "ignore").strip() 
    except:
        seriesNumber    = ""
        seriesName      = ""


    stats       = statSoup.dl.find_all(['dd','dt'])

    words       = str(stats[1].contents[0])
    chapters    = str(stats[3].contents[0])
    comments = 0
    kudos = 0
    bookmarks = 0
    hits = 0
    # print(stats)
    for x in range(0, len(stats)):
        stat_type   = str(stats[x].contents[0]).strip()
        if stat_type == "Comments:":
            comments = str(stats[x+1].contents).strip()
        elif stat_type == "Kudos:":
            kudos = str(stats[x+1].contents[0]).strip()
        elif stat_type == "Bookmarks:":
            bookmarks = str(stats[x+1].a.contents[0]).strip()
        elif stat_type == "Hits:":
            hits = str(stats[x+1].contents[0]).strip()
        elif stat_type == "Words:":
            words = str(stats[x+1].contents[0]).strip()
        elif stat_type == "Chapters:":
            chapters = str(stats[x+1].contents[0]).strip()
        elif stat_type == "Published:":
            PubDate = str(stats[x+1].contents[0]).strip()
        elif stat_type == "Completed:":
            CompletedDate = str(stats[x+1].contents[0]).strip()
    
    storyID = re.search('works/(\d+)',storyURL).group(1)
    storyItems =   { \
        'title':title, \
        'storyURL':storyURL, \
        'authorURL':authorURL, \
        'authorName':authorName, \
        'summary':summary, \
        'kudos':kudos, \
        'bookmarks':bookmarks,
        'words':words, \
        'chapters':chapters, \
        'comments':comments, \
        'relationships':relation_txt,\
        'fandom':fandom,\
        'hits':hits,\
        'ID': storyID,\
        'tags':tagTxt,\
        'seriesName':seriesName,\
        'seriesNumber':seriesNumber,\
        'PubDate':PubDate,\
        'CompletedDate':CompletedDate\
        }
        
    return storyItems


# if test == 1:
#     StatsFromIDURL("")