#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request, urllib.parse
from lxml.html import parse, tostring, fromstring

trackers = {"All": 0 ,"Archlinux": 1 , "AUR": 2, "Community" :5,"Pacman": 3,"ReleaseEngineering":6}

def getflyspraypage(tracker="All",pkgname="",due_in_version=False,status=0,assigned="",openedfrom="",openedto=""):
    """
    Retreive the FlySpray website with custom parameters

    Args:
        tracker - string
        pkgname - string to search
        due_in_version - int  (0 or ""(1), unassigned or due in any version)
        status - int  (open (0),1,3 - all open tasks, unconfirmed, assigned)
        assigned - string ("" or "developer" )
        openedfrom - string (yyyy-mm-dd)
        openedto - string (yyyy-mm-dd)
    Returns:
        string raw html
    """

    url = "https://bugs.archlinux.org/index.php?string=&project=&search_name=&type[]=&sev[]=&pri[]=&due[]=&reported[]=&cat[]=&status[]=open&percent[]=&opened=&dev=&closed=&duedatefrom=&duedateto=&changedfrom=&changedto=&openedfrom=&openedto=&closedfrom=&closedto=&do=index"

    # Format url
    url = url.replace('project=','project=' + str(trackers[tracker]))

    if pkgname != "":
        url = url.replace('string=','string=' + pkgname)
    if due_in_version:
        url = url.replace('due[]=','due[]=0')
    if status != 0:
        url = url.replace('status[]=open','status[]=' + str(status))
    if assigned != "":
        url = url.replace('dev=','dev=' + assigned)

    # TODO: check date
    if openedfrom != "":
        url = url.replace('openedfrom=','openedfrom=' + openedfrom)

    # TODO: check date
    if openedto != "":
        url = url.replace('openedto=','openedto=' + openedto)

    return parse_bugtrackerpage(url)

def getunassignedbugs(tracker):
    """
    Fetches unassigned bugs from a given tracker
    """
    bugs = getflyspraypage(tracker,"",True,1)
    msg = "* [{} FS#{}] - {}"
    print("Unassigned Bugs")
    for bug in bugs:
        print(msg.format(bug['url'],bug['id'],bug['summary']))

def searchbug(tracker,name):
    """
    Fetches bugs filtered by a search string
    """
    bugs = getflyspraypage(tracker,name)
    print("Found Bugs")
    msg = "* [{} FS#{}] - {}"
    for bug in bugs:
        print(msg.format(bug['url'],bug['id'],bug['summary']))

def getoldbugs(tracker,date):
    """
    Fetches bugs openend and still open till a given date
    """
    bugs = getflyspraypage(tracker,"",False,0,"","",date)
    print("Bugs open since {}".format(date))
    msg = "* [{} FS#{}] - {}"
    for bug in bugs:
        print(msg.format(bug['url'],bug['id'],bug['summary']))

def getallbugs(tracker):
    return getflyspraypage(tracker)



def parse_bugtrackerpage(url,count=1):
    # open bugtracker / parse 
    page = urllib.request.urlopen(url)
    doc = fromstring(page.read().decode())

    buglist = []
    pages = False

    # Is there another page?
    if doc.cssselect('td#numbers a#next') != []:
        count += 1
        pages = True

    # Select the tasks table
    bugs = doc.cssselect('table#tasklist_table tbody tr')

    dictbug = {}
    if bugs != []:
        for bug in bugs:

            # Gather bug info
            bugid = bug.cssselect('.task_id a')[0].text
            bugsummary  = bug.cssselect('.task_summary a')[0].get('title')

            # TODO: make replacing saner
            bugsummary = bugsummary.replace("Unconfirmed |","")
            bugsummary = bugsummary.replace("Assigned |","")
            bugsummary = bugsummary.replace("| 0%","")

            bugopendate = bug.cssselect('.task_dateopened')[0].text
            bugstatus = bug.cssselect('.task_status')[0].text
            bugurl = 'https://bugs.archlinux.org/task/{}'.format(bugid)

            # Create bug dict
            dictbug = {'id': bugid, 'summary': bugsummary, 'opendate': bugopendate, 'status': bugstatus, 'url': bugurl}
            buglist.append(dictbug)

    if pages == True:
        new = "%s&pagenum=%s" % (url,count)
        buglist += parse_bugtrackerpage(new,count)

    return buglist

