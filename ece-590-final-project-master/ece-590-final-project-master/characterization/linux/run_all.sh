#!/bin/bash

RUNSCRIPT=run.sh

for TOOLDIR in $(ls -d */)
do
    # For all subdirectories
    if [ -x $TOOLDIR/$RUNSCRIPT ]
    then
        # If run script exists and is executable, run it
        cd $TOOLDIR
        ./$RUNSCRIPT
        cd ..
    fi
done

