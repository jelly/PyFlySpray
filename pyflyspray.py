#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser, cookielib, urllib2, urllib
from lxml.html import parse, tostring, fromstring
import re

def parse_bugtrackerpage(url,count=1):
    # open bugtracker / parse 
    page = urllib.urlopen(url)
    doc = fromstring(page.read())

    msg = ""
    pages = False

    # Is there another page?
    if doc.cssselect('td#numbers a#next') != []:
        count += 1
        pages = True

    print '...'

    bugs = doc.cssselect('td.task_id a')
    if bugs != []:
        # all found bugs on a page
        for foo in bugs:
            title = foo.get('title').replace("Assigned |","")
            title = foo.get('title').replace("| 0%","")
            msg += "* [https://bugs.archlinux.org/task/%s FS#%s] %s \n" % (foo.text,foo.text,title)
    elif bugs == [] and count == 1:
        return 'no bugs found'

    if pages == True:
        new = "%s&pagenum=%s" % (url,count)
        msg += parse_bugtrackerpage(new,count)

    return msg

def gettrackerurl(url,tracker):
        # Data
        trackers = {"Archlinux": 1 , "AUR": 2, "Community" :5,"Pacman": 3,"ReleaseEngineering":6}

        # Fix proj,project
        if tracker in trackers.keys():
            id = trackers[tracker]
            url = url.replace('proj?','proj'+str(id)+'?')
            url = url.replace('project=','project='+str(id))
        else:
            url = 'Not a valid project\nValid projects are: '
            for track in trackers.keys():
                url += track + ' '

        return url

class Bugtracker(object):
    def __init__(self):

        # Retreive user information
        config = ConfigParser.ConfigParser()
        config.read("config.cfg")
        self.user = config.get("data","user")
        self.password = config.get("data","password")
        self.login_page = "https://bugs.archlinux.org/index.php?do=authenticate"
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        output = self.login()

    def login(self):
        "handle login, populate the cookie jar"
        login_data = urllib.urlencode({
            "user_name" : self.user,
            "password" : self.password,
            "remember_login" : "on",
            #"return_to" : None,
        })
        response = self.opener.open(self.login_page, login_data, timeout=10)

        return "".join(response.readlines())

    def getunassigned(self,tracker):
            url = "https://bugs.archlinux.org/index/proj?string=&project=&search_name=&type%5B0%5D=&sev%5B0%5D=&pri%5B0%5D=&due%5B0%5D=0&reported%5B0%5D=&cat%5B0%5D=&status%5B0%5D=1&percent%5B0%5D=&opened=&dev=&closed=&duedatefrom=&duedateto=&changedfrom=&changedto=&openedfrom=&openedto=&closedfrom=&closedto=&do=index&order=dateopened&sort=desc" 
            targeturl = gettrackerurl(url,tracker)
            if 'https' in targeturl:
                print 'Fetching data...'
                return parse_bugtrackerpage(targeturl)
            else:
                return targeturl


    def getassignedbugs(self,maintainer):
        url = "https://bugs.archlinux.org/index.php?string=&project=0&search_name=&type%5B%5D=&sev%5B%5D=&pri%5B%5D=&due%5B%5D=&reported%5B%5D=&cat%5B%5D=&status%5B%5D=open&percent%5B%5D=&opened=&dev=&closed=&duedatefrom=&duedateto=&changedfrom=&changedto=&openedfrom=&openedto=&closedfrom=&closedto=&do=index"
        url = url.replace('dev=','dev='+maintainer)
        print 'Fetching data...'
        return parse_bugtrackerpage(url)

    def getbugsopensince(self,tracker,date):
        if re.match(r"(?:(19|20)[0-9]{2}[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01]))\Z", date):

            url = "https://bugs.archlinux.org/index.php?string=&project=&type%5B%5D=&sev%5B%5D=&pri%5B%5D=&due%5B%5D=&reported%5B%5D=&cat%5B%5D=&status%5B%5D=open&percent%5B%5D=&opened=&dev=&closed=&duedatefrom=&duedateto=&changedfrom=&changedto=&openedfrom=&openedto=bugdate&closedfrom=&closedto=&do=index"
            targeturl = gettrackerurl(url,tracker)
            if 'https' in targeturl:
                targeturl = targeturl.replace('bugdate',date)
                print 'Fetching data...'
                return parse_bugtrackerpage(targeturl)
            else:
                return targeturl
        else:
            return 'Not a valid date format, use yyyy-mm-dd'


if __name__ == "__main__":
    bt = Bugtracker()
    print bt.getunassigned("Archlinux")
    print  bt.getassignedbugs('jelly')
    print  bt.getbugsopensince("Archlinux","2010-06-01")
