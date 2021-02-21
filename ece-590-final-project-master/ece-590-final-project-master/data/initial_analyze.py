#!/bin/python3

import os
import pandas as pd
import scipy as sp
import numpy as np

# Configuration
dx_threshold = .3
count_threshold = .5
drop_tail = True
forward_drop_match = ['tinymembench']
optimistic = True
replace_zeroes = True

# Files to process, taken from current working directory
files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
files = [f for f in files if f.endswith('.csv')]
# files = ['tinymembench_linux_data.csv']

for f in files:
    # Read file in fixed format
    print(f'[] File {f:s}')
    df = pd.read_csv(f, index_col=0, na_values=[''])

    # List of candidate edges
    candidate_edges = []

    for c in df.columns:
        # Process every column
        data = df[c]

        for current, next, block_size in zip(data, data[1:], df.index):
            if current == 0.0 and replace_zeroes:
                # Replace the zero
                current = 0.1

            # Perform edge detection
            diff = next - current
            if diff / current > dx_threshold:
                # Edge detected, add as candidate
                candidate_edges.append(block_size)

    # Post-processing, remove low counts
    candidate_edges, counts = np.unique(candidate_edges, return_counts=True)
    result = pd.DataFrame({'edges': candidate_edges, 'counts': counts})
    result = result[result.counts > (len(df.index) * count_threshold)]
    result = result.drop(columns='counts')

    if drop_tail:
        # See if we need to drop forward or reversed
        forward = any(m in f for m in forward_drop_match)
        iterator = zip(df.index, df.index[1:]) if forward else zip(df.index[::-1], df.index[-2::-1])

        # Post-processing, find series of edges and drop the tail
        for current, next in iterator:
            # Iterate reversed over the possible solutions
            if current in result['edges'].values:
                # Found an edge, remove next solution if exists
                result = result[result.edges != next]

    # Make a row map to obtain latency data
    row_map = {i:i for i in df.index}
    if optimistic:
        # Make the row map optimistic by taking latency data of one block size less
        row_map.update(zip(df.index[::-1], df.index[-2::-1]))

    # Calculate latencies and add to results
    latencies = [df.loc[row_map[e]].mean() for e in result['edges']]
    result['latency'] = latencies

    # Rename and add labels before printing
    result.rename(columns={'edges': 'size'}, inplace=True)
    result['cache'] = [f'L{l}$' for l in range(1, len(result.index)+1)]
    result.set_index('cache', inplace=True)
    print(result)
    print()
