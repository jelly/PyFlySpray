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

    # print all found bugs
    for foo in doc.cssselect('td.task_id a'):
        title = foo.get('title').replace("Assigned |","")
        title = foo.get('title').replace("| 0%","")
        msg += "* [https://bugs.archlinux.org/task/%s FS#%s] %s \n" % (foo.text,foo.text,title)

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
        #<div class="errpadding">Error #7: Login failed, password incorrect!</div>
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




if __name__ == "__main__":
    bt = Bugtracker()
    b= bt.getunassigned("Community")
    print b;
