import operator
import subprocess
import os
import time
import sys
from pyquery import PyQuery as pq

SAVE_DIR="/homes/cmy14/public_html/georgia-dev/exercise/"
AUTH = open('AUTH').readline()
TIMTABLE_LINKS_LIST_FILE = "./timetableLinksList.txt"

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

def extractType(link):
    return link.split(":")[4]

def getExt(link):
    return link.split(".")[-1]

def saveNotes(link):
    def getGiven(i, this):
        link = pq(this).attr("href")
        if link[:9]=="given.cgi":
            d = pq(makeLink(link), headers={"Authorization":AUTH})
            d("a").each(getLink)
        """if link[:12]=="showfile.cgi":
            if pq(this).next().attr("href")[:9]!="given.cgi":
                cls=extractClass(link)
                possibleSubjectTr=pq(this).parents("tr")
                while len(possibleSubjectTr.children("td").eq(1).text().split(" - "))<=1:
                    possibleSubjectTr=possibleSubjectTr.prev()
                subject=possibleSubjectTr.children("td").eq(1).text().split(" - ")[1].split(" ")
                subject = reduce(operator.add, subject)
                name = pq(this).text()
                directory = SAVE_DIR+cls+"/"+subject+"/"+name+"/"
                print "Saving "+name;

                curlSave(makeLink(link), directory, pq(this).text()+".pdf", cate_lastupdated)"""
    def getLink(i, this):
        link = pq(this).attr("href")
        if link[:12]=="showfile.cgi":
            cls=extractClass(link)
            subject = pq(this).parents("body").find("h3").eq(1).text().split(" ")[2:]
            subject = reduce(operator.add, subject)
            name = pq(this).parents("body").find("td[align='right'] b").filter(lambda i, this: pq(this).text()=="Title").parents("td").next().text();
            number = pq(this).parents("body").find("td[align='right'] b").filter(lambda i, this: pq(this).text()=="Number").parents("td").next().text();
            if(len(number)<2):
                number="0"+number
            directory = SAVE_DIR+cls+"/"+subject+"/"+number+". "+name+"/"

            cate_lastupdated = time.strptime(pq(this).parents("td").next().text(), "%a %b %d %H:%M:%S %Y")

            if (extractType(link)=="SPECS" and getExt(pq(this).text())=="pdf") or \
            (extractType(link)=="MODELS" and getExt(pq(this).text())=="pdf") or \
            (extractType(link)=="DATA" and getExt(pq(this).text())=="pdf"):
                curlSave(makeLink(link), directory, pq(this).text(), cate_lastupdated)
    d = pq(link, headers={"Authorization":AUTH})
    d("a").each(getGiven)


f = open(TIMTABLE_LINKS_LIST_FILE)
map(saveNotes, f)
#pq(this).parent("tr").find("td").filter(lambda k,v:pq(v).attr("rowspan")!=None).find("a>img").parent().parent().each(getSubject)
