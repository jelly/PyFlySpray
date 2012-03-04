#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser, cookielib, urllib2, urllib
from lxml.html import parse, tostring, fromstring

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

    print count

    bugs = doc.cssselect('td.task_id a')
    if bugs != []:

        # all found bugs on a page
        for foo in bugs:
            title = foo.get('title').replace("Assigned |","")
            title = foo.get('title').replace("| 0%","")
            msg += "* [https://bugs.archlinux.org/task/%s FS#%s] %s \n" % (foo.text,foo.text,title)
    elif bugs == [] and count == 0:
        return 'no bugs found'

    if pages == True:
        new = "%s&pagenum=%s" % (url,count)
        msg += parse_bugtrackerpage(new,count)

    return msg


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

        # Data
        trackers = {"Archlinux": 1 , "AUR": 2, "Community" :5,"Pacman": 3,"ReleaseEngineering":6}

        # Fix proj,project
        if tracker in trackers.keys():
            id = trackers[tracker]
            url = "https://bugs.archlinux.org/index/proj?string=&project=&search_name=&type%5B0%5D=&sev%5B0%5D=&pri%5B0%5D=&due%5B0%5D=0&reported%5B0%5D=&cat%5B0%5D=&status%5B0%5D=1&percent%5B0%5D=&opened=&dev=&closed=&duedatefrom=&duedateto=&changedfrom=&changedto=&openedfrom=&openedto=&closedfrom=&closedto=&do=index&order=dateopened&sort=desc" 
            url = url.replace('proj?','proj'+str(id)+'?')
            url = url.replace('project=','project='+str(id))
            msg = parse_bugtrackerpage(url)
        else:
            msg = 'Not a valid project\nValid projects are: '
            for track in trackers.keys():
                msg += track + ' '

        return msg

    def getassignedbugs(self,maintainer):
        url = "https://bugs.archlinux.org/index.php?string=&project=0&search_name=&type%5B%5D=&sev%5B%5D=&pri%5B%5D=&due%5B%5D=&reported%5B%5D=&cat%5B%5D=&status%5B%5D=open&percent%5B%5D=&opened=&dev=&closed=&duedatefrom=&duedateto=&changedfrom=&changedto=&openedfrom=&openedto=&closedfrom=&closedto=&do=index"
        url = url.replace('dev=','dev='+maintainer)
        print url
        return parse_bugtrackerpage(url)




if __name__ == "__main__":
    bt = Bugtracker()
    b= bt.getunassigned("Archlinux")
    #b = bt.getassignedbugs('jelly')
    print b;
