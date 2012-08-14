#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request, urllib.parse
from lxml.html import parse, tostring, fromstring

trackers = {"Archlinux": 1 , "AUR": 2, "Community" :5,"Pacman": 3,"ReleaseEngineering":6}


def getflyspraypage(tracker,due_in_version,status,assigned,openedfrom,openedto):
    """
    Retreive the FlySpray website with custom parameters

    Args:
        tracker - string  
        due_in_version - int  (0 or ""(1), unassigned or due in any version)
        status - int  (open (0),1,3 - all open tasks, unconfirmed, assigned)
        assigned - string ("" or "developer" )
        openedfrom - string (yyyy-mm-dd)
        openedto - string (yyyy-mm-dd)
    Returns:
        string raw html
    """
    url = "https://bugs.archlinux.org/index.php?string=&project=1&search_name=&type[]=&sev[]=&pri[]=&due[]=&reported[]=&cat[]=&status[]=open&percent[]=&opened=&dev=&closed=&duedatefrom=&duedateto=&changedfrom=&changedto=&openedfrom=&openedto=&closedfrom=&closedto=&do=index [-]"

    if tracker != "":
        url = url.replace('',trackers[tracker])


    try:
        page = urllib.request.urlopen(url)
    except ValueError:
        print ("Couldn't parse source {0} ".format(url))

    return page.read().decode()

def getarchwebpage(repo,maintainer,pkgname):
    """
    Retreive archweb website with custom parameters

    Args:
        repo - Community,Core,Extra,Multilib
        maintainer - maintainer name
        pkgname - name of the package

    Returns:
        raw html string
    """

    # Format url
    url = "http://www.archlinux.org/packages/?sort=&repo=reponame&q=&maintainer=&last_update=&flagged=&limit=all" 
    url = url.replace('reponame',repo)

    if maintainer != "":
        url = url.replace('maintainer=','maintainer=' + maintainer)

    if pkgname != "":
        url = url.replace('q=','q=' + pkgname)

    try:
        page = urllib.request.urlopen(url)
    except ValueError:
        print ("Couldn't parse source {0} ".format(url))

    return page.read().decode()
    

def getorphans(repo):
    """
    Retreives a list of orphans
    
    Args:
        repo - string
    Returns:
        List of orphans 
    """

    page = getarchwebpage(repo,'','')

    # Declare variables
    olditem =  ""
    orphanlist = []

    # Read html with Lxml.html
    doc = fromstring(page)

    # list of orphans
    orphans =  doc.cssselect('table.results tr td a')

    # Loop over the packages, compare the old package with the new package so we don't have duplicates.
    # This is needed since there are unique i686 and x86_64 bit packages.
    for item in orphans:
        if item.text != olditem:
            orphanlist.append(item.text)
        olditem = item.text

    return orphanlist

def getbugtracker():
    foo = ""

def parse_(url):
    page = urllib.request.urlopen(url)
    doc = fromstring(page.read().decode())





def parse_bugtrackerpage(url,count=1,orphans=[]):
    # open bugtracker / parse 
    page = urllib.request.urlopen(url)
    doc = fromstring(page.read().decode())

    msg = ""
    pages = False

    # Is there another page?
    if doc.cssselect('td#numbers a#next') != []:
        count += 1
        pages = True

    sys.stdout.write('..'*count+'\r')

    bugs = doc.cssselect('td.task_id a')
    if bugs != []:
        # all found bugs on a page
        for foo in bugs:
            title = foo.get('title').replace("Unconfirmed |","")
            title = title.replace("Assigned |","")
            title = title.replace("| 0%","")
            if orphans != []:
                for orphan in orphans:
                    if orphan in title:
                        msg += "* [https://bugs.archlinux.org/task/%s FS#%s] %s \n" % (foo.text,foo.text,title)
            else:
                msg += "* [https://bugs.archlinux.org/task/%s FS#%s] %s \n" % (foo.text,foo.text,title)
    elif bugs == [] and count == 1:
        return 'no bugs found'

    if pages == True:
        new = "%s&pagenum=%s" % (url,count)
        if orphans != []:
            msg += parse_bugtrackerpage(new,count,orphans)
        else:
            msg += parse_bugtrackerpage(new,count)

    return msg

def gettrackerurl(url,tracker):
        # Data
        trackers = {"Archlinux": 1 , "AUR": 2, "Community" :5,"Pacman": 3,"ReleaseEngineering":6}

        # Fix proj,project
        if tracker in trackers:
            id = trackers[tracker]
            url = url.replace('proj?','proj'+str(id)+'?')
            url = url.replace('project=','project=%s' % str(id))
        else:
            url = 'Not a valid project\nValid projects are: '
            for track in trackers:
                url += track + ' '

        return url

class Bugtracker(object):

    def getunassigned(self,tracker):
            url = "https://bugs.archlinux.org/index/proj?string=&project=&search_name=&type%5B0%5D=&sev%5B0%5D=&pri%5B0%5D=&due%5B0%5D=0&reported%5B0%5D=&cat%5B0%5D=&status%5B0%5D=1&percent%5B0%5D=&opened=&dev=&closed=&duedatefrom=&duedateto=&changedfrom=&changedto=&openedfrom=&openedto=&closedfrom=&closedto=&do=index&order=dateopened&sort=desc" 
            targeturl = gettrackerurl(url,tracker)
            if 'https' in targeturl:
                print('Fetching data')
                return parse_bugtrackerpage(targeturl)
            else:
                return targeturl


    def getassignedbugs(self,maintainer):
        url = "https://bugs.archlinux.org/index.php?string=&project=0&search_name=&type%5B%5D=&sev%5B%5D=&pri%5B%5D=&due%5B%5D=&reported%5B%5D=&cat%5B%5D=&status%5B%5D=open&percent%5B%5D=&opened=&dev=&closed=&duedatefrom=&duedateto=&changedfrom=&changedto=&openedfrom=&openedto=&closedfrom=&closedto=&do=index"
        url = url.replace('dev=','dev='+maintainer)
        print('Fetching data')
        return parse_bugtrackerpage(url)

    def getbugsopensince(self,date,tracker):
        if re.match(r"(?:(19|20)[0-9]{2}[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01]))\Z", date):

            url = "https://bugs.archlinux.org/index.php?string=&project=&type%5B%5D=&sev%5B%5D=&pri%5B%5D=&due%5B%5D=&reported%5B%5D=&cat%5B%5D=&status%5B%5D=open&percent%5B%5D=&opened=&dev=&closed=&duedatefrom=&duedateto=&changedfrom=&changedto=&openedfrom=&openedto=bugdate&closedfrom=&closedto=&do=index"
            targeturl = gettrackerurl(url,tracker)
            if 'https' in targeturl:
                targeturl = targeturl.replace('bugdate',date)
                print('Fetching data')
                return parse_bugtrackerpage(targeturl)
            else:
                return targeturl
        else:
            return 'Not a valid date format, use yyyy-mm-dd'

    def getorphanbugs(self,tracker):
        if tracker == 'Community':
            orphanurl = "http://www.archlinux.org/packages/?sort=&repo=Community&q=&maintainer=orphan&last_update=&flagged=&limit=all" 
            bugsurl = "https://bugs.archlinux.org/index.php?string=&project=5&search_name=&type%5B%5D=&sev%5B%5D=&pri%5B%5D=&due%5B%5D=0&reported%5B%5D=&cat%5B%5D=&status%5B%5D=1&percent%5B%5D=&opened=&dev=&closed=&duedatefrom=&duedateto=&changedfrom=&changedto=&openedfrom=&openedto=&closedfrom=&closedto=&do=index"
        elif tracker == 'Archlinux':
            orphanurl ="http://www.archlinux.org/packages/?sort=&repo=Core&repo=Extra&repo=Testing&q=&maintainer=orphan&last_update=&flagged=&limit=all"
            bugsurl = "https://bugs.archlinux.org/index.php?string=&project=1&search_name=&type%5B%5D=&sev%5B%5D=&pri%5B%5D=&due%5B%5D=0&reported%5B%5D=&cat%5B%5D=&status%5B%5D=open&status%5B%5D=1&percent%5B%5D=&opened=&dev=&closed=&duedatefrom=&duedateto=&changedfrom=&changedto=&openedfrom=&openedto=&closedfrom=&closedto=&do=index"
        else:
            return "not a valid tracker"

        page = urllib.request.urlopen(orphanurl)
        doc = fromstring(page.read().decode())
        # list of orphans
        foo =  doc.cssselect('table.results tr td a')

        outlist = unify(foo)
        print('Fetching data')
        return parse_bugtrackerpage(bugsurl,1,outlist)
    def getorphans(self,tracker):
        if tracker == 'Community':
            orphanurl = "http://www.archlinux.org/packages/?sort=&repo=Community&q=&maintainer=orphan&last_update=&flagged=&limit=all" 
        elif tracker == 'Archlinux':
            orphanurl ="http://www.archlinux.org/packages/?sort=&repo=Core&repo=Extra&repo=Testing&q=&maintainer=orphan&last_update=&flagged=&limit=all"
        else:
            return "not a valid tracker"

        page = urllib.request.urlopen(orphanurl)
        doc = fromstring(page.read().decode())
        # list of orphans
        foo =  doc.cssselect('table.results tr td a')
        for item in foo:
            msg = "* %s - http://archlinux.org%s" % (item.text,item.get('href'))
            print (msg)
