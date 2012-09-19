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
    url = url.replace('project=','project=' + trackers[tracker])

    if pkgname != "":
        url = url.replace('string=','string=' + pkgname)
    if due_in_version:
        url = url.replace('due[]=','due[]=0')
    if status != 0:
        url = url.replace('status[]=','status[]=' + status)
    if assigned != "":
        url = url.replace('dev=','dev=' + assigned)

    # TODO: check date
    if openedfrom != "":
        url = url.replace('openedfrom=','openedfrom=' + openedfrom)

    # TODO: check date
    if openedto != "":
        url = url.replace('openedto=','openedto=' + openedto)

    try:
        page = urllib.request.urlopen(url)
    except ValueError:
        print ("Couldn't parse source {0} ".format(url))

    return page.read().decode()

