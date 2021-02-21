#!/bin/bash -e

# Prepare results folder
mkdir -p results

# Run
FNAME="results/$(date -Iseconds)-$HOSTNAME.out"
cat /proc/cpuinfo > $FNAME
cat /proc/meminfo >> $FNAME

