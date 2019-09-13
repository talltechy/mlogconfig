#!/usr/bin/env python3
import os
import sys

folder = 'C:/Users/YOURPATHHERE'
for filename in os.listdir(folder):
       infilename = os.path.join(folder,filename)
       if not os.path.isfile(infilename): continue
       oldbase = os.path.splitext(filename)
       newname = infilename.replace('.pgsql', '.sql')
       output = os.rename(infilename, newname)