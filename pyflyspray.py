#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request, urllib.parse
from lxml.html import parse, tostring, fromstring
import argparse, re,sys

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
            url = url.replace('project=','project='+str(id))
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
        new = []
        for f in foo:
            f = f.text
            new.append(f)
        print('Fetching data')
        return parse_bugtrackerpage(bugsurl,1,new)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interface to the Archlinux Bugtracker')
    parser.add_argument('-u','--unassigned', help='Fetch unassigned bugs from Archlinux,AUR,Community,Pacman or ReleaseEngineering', required=False)
    parser.add_argument('-a','--assigned', help='Fetch assigned bugs by given maintainer from bugs.archlinux.org', required=False)
    parser.add_argument('-o','--openbugs', help='Fetch open bugs since given date yyyy-mm-dd and tracker', required=False,nargs=2)
    parser.add_argument('-b','--orphanbugs', help='Fetch orphan bugs from Archlinux or Community', required=False)
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = vars(parser.parse_args())
    bt = Bugtracker()
    if args['unassigned']:
        print (bt.getunassigned(args['unassigned']))
    if args['assigned']:
        print (bt.getassignedbugs(args['assigned']))
    if args['openbugs']:
        print (bt.getbugsopensince(args['openbugs'][0],args['openbugs'][1]))
    if args['orphanbugs']:
        print (bt.getorphanbugs(args['orphanbugs']))
