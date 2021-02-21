#!/bin/python3

import os
import pandas as pd
import scipy as sp
import numpy as np
import statistics
import matplotlib.pyplot as plt
import matplotlib.colors

# Files to process, taken from current working directory
files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
files = [f for f in files if f.endswith('.csv')]
# print(files)
#files = ['tinymembench_linux_data.csv', 'tinymembench_vmlinux_data.csv', 'tinymembench_windows_data.csv']
#files =  ['intelmlc_linux_data.csv',  ]
#files = ['intelmlc_windows_data.csv']
#files = ['lmbench_linux_data.csv']

# Define configuration object
class Config:
    def __init__(self, block_adjustment, dx_threshold, replace_negatives, replace_zeros, compare_counts, optimistic):
        self.block_adjustment = block_adjustment
        self.dx_threshold = dx_threshold
        self.replace_negatives = replace_negatives
        self.replace_zeros = replace_zeros
        self.compare_counts = compare_counts
        self.optimistic = optimistic

# Process each file        
for f in files:

    # Set configuration for each benchmark 
    if ('intelmlc' in f):
        config = Config(1, 0, True, False, True, False) 
    if ('lmbench' in f):
        config = Config(1024*0.000001, 0, True, False, True, False)
    if ('tinymembench' in f):
        config = Config(1024, 0, True, True, True, False)

    # Read file in fixed format
    print(f'[] File {f:s}')
    
    # Initialize processing variables created once per file
    df = pd.read_csv(f, index_col=0, na_values=[''])
    df_edges = pd.read_csv(f, index_col=0, na_values=['']) # values will be replaced with calcuelated edges
    blocks_all = np.array(df.index/config.block_adjustment) # block sizes
    avg_edges_by_col = []
    detected_edge_blocks = []
    report_edges_all = [] 
    report_edges_filtered = []

    #print('df', df)

    # Process each column
    for c in df.columns:

        # Initialize variables created once per trial
        latencies_all = np.array(df[c]) # df[c].values
        edges_all = [] 
        avg_edge = 0
        dx = 0
        
        latencies_padded = []

        # Pre-process data and calculate edges
        for current, next, block_size in zip(latencies_all, latencies_all[1:], blocks_all):

            diff = next - current

            if config.replace_negatives:
                if current > next:
                    diff = 0

            # Avoid zeros and noise
            if config.replace_zeros:
                if current < 1 and next < 1:
                    diff = 0
                    current = 1
                 
                if current < 1 and next >= 1: 
                    current = 1
                    next = next + 1 
                    diff = next - current    
            
            edge = diff / current
            edges_all.append(edge)
            report_edges_all.append(edge)

        # Get average edge size and set dx_threshold
        avg_edge = np.mean(edges_all)
       # print("avg_edge", avg_edge)
        avg_edges_by_col.append(avg_edge)
        #print ("avg_edges", avg_edges)

        edges_all.append(0) # to match size of blocks_all

        if ('intelmlc' in f):
            config.dx_threshold = 0.75*avg_edge
        if ('lmbench' in f):
            config.dx_threshold = avg_edge
        if ('tinymembench' in f):
            config.dx_threshold = 1.25*avg_edge
       

        #print("trial dx", config.dx_threshold)

        # Check if edge is over edge detection threshold
        for i in range(len(edges_all)):
            #print(i, edges_all[i])
            if edges_all[i] > config.dx_threshold:
                latencies_padded.append(latencies_all[i])
                detected_edge_blocks.append(blocks_all[i])
                report_edges_filtered.append(edges_all[i])
            else:
                latencies_padded.append("") # want to overwrite values


        # Update dataframes
        col_padded = pd.DataFrame({c: latencies_padded}, index=blocks_all)
        df.update(col_padded)
        
        col_edges = pd.DataFrame({c: edges_all}, index=blocks_all)
        df_edges.update(col_edges)


    """ End trial processing """

    #print(df)
    #print(df_edges)

    """ Values used only for report """

    report_edge_avg = np.mean(avg_edges_by_col)
    report_edge_std = statistics.stdev(avg_edges_by_col)
    print("benchmark", f, "avg", report_edge_avg, "std", report_edge_std)

    """ Post-processing: compare counts and edge sizes """

    # Initialize post-processing variables created once per file  
    df2 = pd.read_csv(f, index_col=0, na_values=[''])
    avg_latencies_by_row = []
    avg_edges_by_row = []
    candidates = []
    candidate_blocks = []
    counts = []
    candidate_latencies = []
    candidate_edges = []
    blocks_padded = []

    # Get unique blocks and average latency, average edge size, and count per block
    candidate_blocks, counts = np.unique(detected_edge_blocks, return_counts=True)
    
    avg_latencies_by_row = df2.mean(axis=1).values
    avg_edges_by_row = df_edges.mean(axis=1).values

    for i in range(len(blocks_all)):
        for j in range(len(candidate_blocks)):
            if blocks_all[i] == candidate_blocks[j]:
                candidate_latencies.append(avg_latencies_by_row[i])
                candidate_edges.append(avg_edges_by_row[i])
                blocks_padded.append(candidate_blocks[j])
                break
            elif j == (len(candidate_blocks) - 1):
                blocks_padded.append("")

    # Traverse candidate blocks for clusters
    clusters = []
    cluster = []

    for i in range(len(blocks_all)):
        if blocks_all[i] == blocks_padded[i]:
                cluster.append(blocks_padded[i])
        else:
            if len(cluster) > 0:
                clusters.append(cluster)
                cluster = []
            else:
                cluster = cluster

    print("clusters", clusters)

    # Put candidate edges in a DataFrame
    result = pd.DataFrame({'latency': candidate_latencies, 'edge_size': candidate_edges, 'count': counts}, index=candidate_blocks)
    #print(result)

    # Apply drop method to each cluster: drop lowest count until one candidate per cluster; if counts match, drop based on edge size
    for i in range(len(clusters)): 
        #print("i", i)
        if len(clusters[i]) > 1:

            while len(clusters[i]) > 1:
                # Initialize vars every time a candidate is removed
                cluster_counts = [] 
                min_count = np.max(result.loc[: , 'count'])
                cluster_edges = []
                min_edge = np.max(result.loc[: , 'edge_size'])

                if config.compare_counts:
                    for j in range(len(clusters[i])):
                        
                        count_curr = result.loc[clusters[i][j], 'count'] # get count of current element and add to list
                        cluster_counts.append(count_curr) 
                        min_count = min(cluster_counts)

                        edge_curr = result.loc[clusters[i][j], 'edge_size']
                        cluster_edges.append(edge_curr)
                        min_edge = min(cluster_edges)

                        # Set index of candidate to drop 
                        if count_curr == min_count:
                            if cluster_counts.count(min_count) == 1:
                                elem = clusters[i][j] # update element to remove
                            if (cluster_counts.count(min_count) > 1) and (j == len(clusters[i]) - 1):
                                for k in range(len(cluster_edges)): # k effectively resets j
                                    if cluster_edges[k] == min_edge:
                                        elem = clusters[i][k] 


                    #print("element", elem, min_count, min_edge)
                    result = result.drop([elem], axis=0)
                    clusters[i].remove(elem) # effectively decrementing the while loop iter
    print(result)
        
    """           
    result_optimistic = pd.DataFrame({'block_size': candidate_blocks, 'latency': candidate_latencies})

    # Make a row map to obtain latency data
    row_map = {i:i for i in blocks_all}
    if config.optimistic:
        # Make the row map optimistic by taking latency data of one block size less
        row_map.update(zip(df.index[::-1], df.index[-2::-1]))

    # Calculate latencies and add to results
    latencies = [df.loc[row_map[b]].mean() for b in candidate_blocks]
    result_optimistic['latency'] = latencies

    # Rename and add labels before printing
    result.rename(columns={'edges': 'size'}, inplace=True)
    result['cache'] = [f'L{l}$' for l in range(1, len(result.index)+1)]
    result.set_index('cache', inplace=True)
    print(result_optimistic)
    print()
    """ 
