#!/bin/bash -e

# Prepare results folder
mkdir -p results

if [ ! -d lmbench3 ]
then
    # Download archive
    wget -nc "http://www.bitmover.com/lmbench/lmbench3.tar.gz"

    # Extract archive
    tar -xvzf lmbench3.tar.gz

    # Patch cache.c
    chmod +w lmbench3/src/cache.c
    patch lmbench3/src/cache.c < patch_cache.diff
fi

# Move into directory
cd lmbench3

# Fix for missing file (otherwise a compilation error will occur)
mkdir -p SCCS
touch SCCS/s.ChangeSet

# Build
CFLAGS="-O2 -march=native -mtune=native"
make

# Only run cache tool
./bin/x86_64-linux-gnu/cache &> ../results/$(date -Iseconds)_$HOSTNAME.out

