#!/usr/bin/env python3
import os
import dir_exclude
import dir_startdir

for root, dirs, files in os.walk(dir_startdir.startdir):
    dirs[:] = [d for d in dirs if d not in dir_exclude.exclude]
    for filename in files: 
        infilename = os.path.join(root,filename)
        newname = infilename.replace('.pgsql', '.sql')
        output = os.rename(infilename, newname)