#!/bin/bash -e

# Prepare results folder
mkdir -p results

if [ ! -d mlc ]
then
    # Prepare unpack folder
    mkdir -p mlc
    # Extract archive
    tar -xvzf mlc_v3.8.tgz -C mlc
fi

# Output file
OFILE="results/$(date -Iseconds)_$HOSTNAME.out"
# Static arguments to mlc tool
ARGS="--idle_latency -c0 -t20 -e -r"

# Report args
echo "Executing mlc using the following static args: $ARGS" >> $OFILE
echo >> $OFILE

# Execute the actual commands
for (( B=32; B<=64000; B=2*B ))
do
    echo "Testing with a buffer size of $B KB..." >> $OFILE
    ./mlc/Linux/mlc $ARGS -b$B >> $OFILE
    echo >> $OFILE
done

