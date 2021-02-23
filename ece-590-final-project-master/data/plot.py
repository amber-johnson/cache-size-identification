#!/bin/python3

import os
import pandas as pd
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

# Files to process, taken from current working directory
files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
files = [f for f in files if f.endswith('.csv')]
# print(files)
#files = ['tinymembench_linux_data.csv']
#files = ['tinymembench_windows_data.csv']
#files = ['intelmlc_linux_data.csv', 'intelmlc_vmlinux_data.csv', 'intelmlc_windows_data.csv', 'tinymembench_linux_data.csv', 'tinymembench_vmlinux_data.csv', 'tinymembench_windows_data.csv']
#files =  ['intelmlc_linux_data.csv',  ]
#files = ['intelmlc_windows_data.csv']
#files = ['lmbench_linux_data.csv']

tmb = ('Tinymembench (-L1$ latency)', 1024)
imlc = ('Intel MLC', 1024 / 1000)
lmb = ('LMbench', 1024 * 0.000001)

m1 = {'tinymembench_linux_data.csv': tmb,
      'intelmlc_linux_data.csv': imlc,
      'lmbench_linux_data.csv': lmb,}
m2 = {'tinymembench_vmlinux_data.csv': tmb,
      'intelmlc_vmlinux_data.csv': imlc,
      'lmbench_vmlinux_data.csv': lmb,}
m3 = {'tinymembench_windows_data.csv': tmb,
      'intelmlc_windows_data.csv': imlc,
      'lmbench_data_withEmptyCells/lmbench_windows_data.csv': lmb,
      }

benchmarks = {'machine_1.pdf': m1, 'machine_2.pdf': m2, 'machine_3.pdf': m3}

x_ticks_base = [2**i for i in range(3, 14)]
y_ticks = [1, 3, 10, 30, 100]

for output_file, data in benchmarks.items():

    # Nasty hack to make x axis of machine 2 span over a larger range
    m2_hack = '2' in output_file
    x_ticks = [2**i for i in range(3, 16)] if m2_hack else x_ticks_base

    plt.figure(figsize=(6,3.5))
    
    for file_name, (bench_name, block_scalar) in data.items():
        # Read file
        print(f'[] File {file_name:s}')
        df = pd.read_csv(file_name, na_values=[''])
        
        # Scale index
        df['buffer_size'] /= block_scalar
        
        # Remove data outside of view range
        #df = df[x_ticks[0] <= df['buffer_size'] <= x_ticks[-1]]
        range_filter = ((df['buffer_size'] >= x_ticks[0]) & (df['buffer_size'] <= x_ticks[-1]))
        df = df[range_filter]
        
        # Set index
        df = df.set_index('buffer_size')
        
        # Statistics per row
        df['mean'] = df.mean(axis=1)
        df['std'] = df.std(axis=1)
        
        # Plot
        plt.errorbar(df.index, df['mean'], df['std'], fmt='o', label=bench_name)
        
    # Finalize plot
    plt.xscale('log')
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='minor',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False)
    if m2_hack:
        x_ticks_labels = [str(t) if t not in {1024, 4096, 16384} else '' for t in x_ticks]
        plt.xticks(x_ticks, x_ticks_labels)
    else:
        plt.xticks(x_ticks, [str(i) for i in x_ticks])
    plt.ylim(bottom=0.8)
    plt.xlabel(f'Block size (KiB)')
    
    plt.yscale('log')
    #plt.tick_params(
    #    axis='y',          # changes apply to the x-axis
    #    which='minor',      # both major and minor ticks are affected
    #    bottom=False,      # ticks along the bottom edge are off
    #    top=False)
    plt.yticks(y_ticks, [str(i) for i in y_ticks])
    plt.ylabel('Latency (ns)')
    
    plt.legend(loc='upper left')
    plt.savefig(output_file, bbox_inches='tight')
    plt.clf()

