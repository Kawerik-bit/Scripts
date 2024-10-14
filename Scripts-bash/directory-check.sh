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
