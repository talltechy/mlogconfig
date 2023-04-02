#!/usr/bin/env python3
import os
import dir_exclude
import dir_startdir

try:
    for root, dirs, files in os.walk(dir_startdir.startdir):
        dirs[:] = [d for d in dirs if d not in dir_exclude.exclude_list]
        for filename in files:
            if filename.endswith('.pgsql'): # Check if file name ends with .pgsql
                infilename = os.path.join(root,filename)
                newname = infilename.replace('.pgsql', '.sql')
                try:
                    output = os.rename(infilename, newname)
                except Exception as e:
                    print(f"Error occurred: {e}") # Handle any exception that occurs during file renaming
except Exception as e:
    print(f"Error occurred: {e}") # Handle any exception that occurs during os.walk
