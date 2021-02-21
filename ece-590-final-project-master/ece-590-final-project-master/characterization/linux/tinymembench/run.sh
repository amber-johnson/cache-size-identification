#!/bin/bash -e

# Prepare results folder
mkdir -p results

if [ ! -d tinymembench ]
then
    # Download repository
    git clone "git@github.com:ssvb/tinymembench.git"
fi

# Move into directory
cd tinymembench

# Build
CFLAGS="-O2 -march=native -mtune=native"
make

# Run
./tinymembench > ../results/$(date -Iseconds)-$HOSTNAME.out

