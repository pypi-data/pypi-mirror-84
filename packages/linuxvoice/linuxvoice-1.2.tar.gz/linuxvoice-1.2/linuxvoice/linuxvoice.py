#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2020  Rajagiri SET <https://www.rajagiritech.ac.in/>

This file is part of Dollect - this file does automated download of LINUXVOICE issues.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details. 

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""

import wget
import sys
import os
import urllib
# from pathlib import Path
from os.path import expanduser
#from BeautifulSoup import *

global stringa
global stringb
global formataccept
formataccept = "initial"
global arca
arca = "initial"
global selection
selection = "initial"
global form
form = "initial"
global dlink
dlink = 0
global text
text = "initial"
stringa = "(TRANS...> "
stringb = ".pdf"

def lva():
    stringc = "http://www.linuxvoice.com/issues/00"
    stringd = "/Linux-Voice-Issue-00"
    stringg = "Linux-Voice-Issue-00"
    c = stringc  + str(i)  + stringd 
    d =  str(i) + stringb
   # home = str(Path.home())
 #   home = expanduser("~")
    try:
        if (i >= 1 and i <= 9):
            if os.path.exists(stringg+d):
                exit()
            filename = wget.download(c+d)
    except:
        print ("\n SKIP: the file may elready exist \n")
    
def lvb():
    stringe = "/Linux-Voice-Issue-0"
    stringf = "http://www.linuxvoice.com/issues/0"
    stringh = "Linux-Voice-Issue-0"
   # home = str(Path.home())
   #  home = expanduser("~")
    if (i > 27 and i <= 32):
        stringf = "http://www.linuxvoice.com/issues/"
        a = stringf
        b = stringe + str(i) + stringb
        if os.path.exists(b):
            print ("\n SKIP: the file may elready exist \n")
            exit()
        filename = wget.download(a+b)
    else:
        a = stringf + str(i)  + stringe
        b = str(i) + stringb
        if os.path.exists(stringh+b):
            print ("\n SKIP: the file may elready exist \n")
            exit()
        filename = wget.download(a+b)

if len(sys.argv) > 1:
    if sys.argv[1] == "lv" and len(sys.argv) == 3:
        if int(sys.argv[2]) <= 9:
#            print "hello"
            i = int(sys.argv[2])
            lva()
            sys.exit(0)
        elif int(sys.argv[2]) <= 32:
            #debug
            i = int(sys.argv[2])
            lvb()
            sys.exit(0)      
    else:
        print ("\n LINUXVOICE COMPLETE \n")
        for i in range(33):
            if i == 0:
                continue
            if i <= 9:
                lva()
            else:
                lvb()
