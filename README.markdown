PyFlySpray
==========
An tool to view or get information from Archlinux's bugtracker.

Dependencies
------------
* python 3
* lxml


Features
--------

* Retreive unassigned bugs by tracker  (AUR,Archlinux,Community,Pacman,ReleaseEngineering)
* Retreive assigned bugs per maintainer
* Retreive bugs that are from any give date 
* Retreive orphans with bugs 
* Retreive orphans from archweb 

Usage
-----
usage: pyflyspray.py [-h] [-u UNASSIGNED] [-a ASSIGNED] [-o OPENBUGS OPENBUGS]
                     [-b ORPHANBUGS] [-s ORPHANS] [--version]

Interface to the Archlinux Bugtracker

optional arguments:
  -h, --help            show this help message and exit
  -u UNASSIGNED, --unassigned UNASSIGNED
                        Fetch unassigned bugs from
                        Archlinux,AUR,Community,Pacman or ReleaseEngineering
  -a ASSIGNED, --assigned ASSIGNED
                        Fetch assigned bugs by given maintainer from
                        bugs.archlinux.org
  -o OPENBUGS OPENBUGS, --openbugs OPENBUGS OPENBUGS
                        Fetch open bugs since given date yyyy-mm-dd and
                        tracker
  -b ORPHANBUGS, --orphanbugs ORPHANBUGS
                        Fetch orphan bugs from Archlinux or Community
  -s ORPHANS, --orphans ORPHANS
                        Fetch orphans from Archlinux or Community
  --version             show program's version number and exit

