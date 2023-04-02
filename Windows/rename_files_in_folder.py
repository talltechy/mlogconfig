# This code renames all files ending with .pgsql to .sql, except for those in the exclude_list
# This code is used as a part of a larger program that is used to create a database from sql files
# The code is executed by the user, and the result is the renaming of the files in the startdir
# The user is prompted for the startdir and exclude_list, and the code is executed on the files in the startdir
# The user is prompted for the startdir and exclude_list, and the code is executed on the files in the startdir
# The code is executed in the following steps:
# 1. The user is prompted for the startdir and exclude_list
# 2. The code iterates through all files in the startdir, and all subdirectories, except those in the exclude_list
# 3. If the file ends with .pgsql, the file is renamed to end with .sql

#!/usr/bin/env python3
import os
import dir_exclude
import dir_startdir

for root, dirs, files in os.walk(dir_startdir.startdir):
    dirs[:] = [d for d in dirs if d not in dir_exclude.exclude_list]
    for filename in files:
        if filename.endswith('.pgsql'):
            infilename = os.path.join(root,filename)
            newname = infilename.replace('.pgsql', '.sql')
            try:
                output = os.rename(infilename, newname)
                print(f"File renamed from {infilename} to {newname}")
            except Exception as e:
                print(f"Error occurred: {e}")
