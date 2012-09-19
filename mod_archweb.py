#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import urllib.request, urllib.parse
from lxml.html import parse, tostring, fromstring

# Base url 
repository = ['All','Community-Testing','Core','Extra','Testing','Multilib']

def getarchwebpage(repo,maintainer="",pkgname="",flagged=""):
    """
    Retreive archweb website with custom parameters

    Args:
        repo - All,Community-Testing,Core,Extra,Multilib,Testing
        maintainer - maintainer name
        pkgname - name of the package
        flagged - All,None

    Returns:
        raw html string
    """
    url = "http://www.archlinux.org/packages/?sort=&repo=reponame&q=&maintainer=&last_update=&flagged=&limit=all" 

    # Format url
    if repo in repository:
        if repo == 'All':
            url = url.replace('&repo=reponame','')
        else:
            url = url.replace('reponame',repo)

    if maintainer != "":
        url = url.replace('maintainer=','maintainer=' + maintainer)

    if pkgname != "":
        url = url.replace('q=','q=' + pkgname)

    if flagged == "All" or flagged == "None":
        url = url.replace('flagged=','flagged=' + flagged)

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

    page = getarchwebpage(repo,'orphan')

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
