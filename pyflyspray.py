#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, re,sys
from mod_pyflyspray import *




if __name__ == "__main__":
    Trackers = ['Archlinux','Community','AUR','Pacman','ReleaseEngineering']
    parser = argparse.ArgumentParser(description='Interface to the Archlinux Bugtracker')
    parser.add_argument('-u','--unassigned', help='Fetch unassigned bugs from Archlinux,AUR,Community,Pacman or ReleaseEngineering',choices=Trackers, required=False)
    parser.add_argument('-a','--assigned', help='Fetch assigned bugs by given maintainer from bugs.archlinux.org', required=False)
    parser.add_argument('-o','--openbugs', help='Fetch open bugs since given date yyyy-mm-dd and tracker',required=False,nargs=2)
    parser.add_argument('-b','--orphanbugs', help='Fetch orphan bugs from Archlinux or Community',choices=Trackers[:2], required=False)
    parser.add_argument('-s','--orphans', help='Fetch orphans from Archlinux or Community', choices=Trackers[:2], required=False)
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = vars(parser.parse_args())
    bt = Bugtracker()
    if args['unassigned']:
        print (bt.getunassigned(args['unassigned']))
    elif args['assigned']:
        print (bt.getassignedbugs(args['assigned']))
    elif args['openbugs']:
        print (bt.getbugsopensince(args['openbugs'][0],args['openbugs'][1]))
    elif args['orphanbugs']:
        print (bt.getorphanbugs(args['orphanbugs']))
    elif args['orphans']:
        print (bt.getorphans(args['orphans']))
    else:
        parser.print_help()
