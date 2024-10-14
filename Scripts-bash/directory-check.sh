#!/bin/bash
echo "Please enter the full directory path you wish to search for:"
read path
echo "Looking ..... "
if [ -d $path ]
then 
   echo "Directory found"
else
   echo "Directory not found"
fi

# execute sith "./directory-check.sh"
# execute it while being in the directory of the script or specify the path to it
