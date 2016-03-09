import operator
import subprocess
import os
import time
#print "last modified: %s" % time.ctime(os.path.getmtime(file))
from pyquery import PyQuery as pq

SAVE_DIR="/homes/cmy14/public_html/georgia-dev/pdf/"
AUTH = open('AUTH').readline()
NOTES_LINKS_LIST_FILE="./notesLinksList.txt"

def touchDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        subprocess.call(["chmod","755",directory])

def curlSave(url, d, fname, cate_lastupdated):
    touchDir(d)
    if (not os.path.exists(d+fname)) or (time.strptime(time.ctime(os.path.getmtime(d+fname)))<cate_lastupdated):
        f=open(d+fname,"w")
        if not os.path.exists(d+fname):
            print fname+" was missing, but added now."
        else:
            print fname+" was out dated, but updated now."
        subprocess.call(["curl","-H","Authorization: "+AUTH,url], stdout=f)
        subprocess.call(["chmod","644",d+fname])
    else:
        print fname+" is up to date."

def makeLink(l):
    return "https://cate.doc.ic.ac.uk/"+l;

def extractClass(link):
    return link.split(":")[3]


def saveNotes(link):
    def getLink(i, this):
        link = pq(this).attr("href")
        if link[:12]=="showfile.cgi":
            ext = pq(this).parents("td").next().text()
            number = pq(this).parents("td").prev().text()
            if(len(number)<2):
                number="0"+number
            name = pq(this).text()
            courseName = d("h3").eq(1).text().split(" ")[2:]
            courseName = reduce(operator.add, courseName)
            cls=extractClass(link)
            directory = SAVE_DIR+cls+"/"+courseName+"/"

            cate_lastupdated = time.strptime(pq(this).parents("td").next().next().next().text(), "%a %b %d %H:%M:%S %Y")
            if(ext == "pdf"):
                curlSave(makeLink(link), directory, number+". "+name+"."+ext, cate_lastupdated)
    d = pq(link, headers={"Authorization":AUTH})
    d("a").each(getLink)



f = open(NOTES_LINKS_LIST_FILE)
map(saveNotes, f)
