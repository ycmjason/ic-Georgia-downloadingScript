import operator
import subprocess
import os
from pyquery import PyQuery as pq

SAVE_DIR="~/public_html/georgia-dev/pdf/"
NOTES_LINKS_LIST_FILE = "./notesLinksList.txt"
TIMTABLE_LINKS_LIST_FILE = "./timetableLinksList.txt"

AUTH = open('AUTH').readline()
PERIODS = ["1","2","3","4","5"]
#["c1","c2","c3","c4","j1","j2","j3","j4","i2","i3","i4","v5","s5","a5","r5","y5","b5"]
CLS_LIST = ["c2"]
YEAR = "2015"

def touchDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def makeLink(l):
    return "https://cate.doc.ic.ac.uk/"+l;

def makeTimetableLinksList():
  #https://cate.doc.ic.ac.uk/timetable.cgi?keyt=2014:3:c1:cmy14
  tl =[]
  for c in CLS_LIST:
    for p in PERIODS:
      tl.append(makeLink("timetable.cgi?keyt="+YEAR+":"+p+":"+c+":cmy14"))
  return tl

def getNotesLinks(link):
    nl=[]
    def getLink(i, this):
        link = pq(this).attr("href")
        if link[:9]=="notes.cgi":
            link=makeLink(link)
            nl.append(link)
            print "Remembered "+link
    d = pq(link, headers={"Authorization":AUTH})
    print "Fetched "+link
    d("a").each(getLink)
    return nl
    
def writeNotesLinksListFile(ls):
  f = open(NOTES_LINKS_LIST_FILE, "w")
  f.writelines(map(lambda x:x+'\n',ls))

def writeTimetableLinksListFile(ls):
  f = open(TIMTABLE_LINKS_LIST_FILE, "w")
  f.writelines(map(lambda x:x+'\n',ls))

tl = makeTimetableLinksList()
writeTimetableLinksListFile(tl)
nl = reduce(operator.add, map(getNotesLinks, tl))
writeNotesLinksListFile(nl)
