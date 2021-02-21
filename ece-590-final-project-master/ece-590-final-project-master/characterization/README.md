# Characterization

This folder contains the files required to characterize the memory hierarchy of systems.
The files are organized in directories per operating system.
More information about characterization tools per operating system can be found in the according folders.

# Machine specifications

This section lists the specifications of machines that we are characterizing.
Some specifications are not provided by the vendor but by third parties instead.

## Leon's laptop

Intel ARK and reported specs:

- CPU: Intel Core i7-6600U (Skylake, 6th generation, stepping 3)
- Launch date: Q3'15
- Lithography: 14 nm
- # of cores: 2
- # of threads: 2 (HT disabled in BIOS)
- Clock: 2.60 GHz (turbo 3.40 GHz) (observed most often around 3.2 GHz)
- Cache: 4 MB
- Memory type: DDR4
- Memory size: 16 GB
- Max memory bandwidth: 34.1 GB/s

[Wikpedia](https://en.wikipedia.org/wiki/Skylake_(microarchitecture)) reported specs for Skylake:

- L1D$: 32 KB
- L1I$: 32 KB
- L2$: 256 KB per core
- L3: 4 MB
- Clock: 2.4 GHz, 3.4 GHz single core turbo, 3.2 GHz dual core turbo

Skylake specs reported by [7-cpu.com](https://www.7-cpu.com/cpu/Skylake.html):

- L1D$: 32 KB, 64 B/line, 8-way, 4 cycles
- L1I$: 32 KB, 64 B/line, 8-way
- L2$: 256 KB, 64 B/line, 4-way, 12 cycles
- L3$: 8 MB, 64 B/line, 16-way, 42 cycles
- Memory: 42 cycles + 51 ns

Other notes:

- Measured clock during benchmarking 3.2 GHz
- Clock period: 0.38 ns (base), 0.29 ns (single core turbo), 0.31 ns (dual core turbo)

### Preliminary results

So far, the preliminary results are in agreement on cache size.
Cache sizes match the expected sizes based on specifications.
Latency in cycles is measured based on a 3.2 GHz clock.
Both benchmarks use `<sys/time.h>` for measuring time.
The number of samples is increased to improve the precision.

lmbench_cache

- L1D$: 32 KB, 1.32 ns latency, 64 linesize -> 4.2 cycles latency
- L2$: 256 KB, 3.54 ns latency, 128 linesize -> 11.3 cycles latency
- L3$: 4 MB, 9.38 ns latency, 256 linesize -> 30.0 cycles latency
- mem: 99.47 ns latency -> 318.3 cycles latency

tinymembench (uses microsecond resolution timer?)

- L1D$: 32 KB, T ns latency
- L2$: 256 KB, T+1.8 ns latency -> +5.8 cycles latency
- L3$: 4 MB, T+12.8 ns latency -> +41.0 cycles latency

## vm.duke.edu

Intel ARK and reported specs:

- CPU: Intel Xeon Gold 6140 (Skylake, stepping 1)
- Launch date: Q3'17
- Lithography: 14 nm
- # of cores: 1 (available to the VM)
- # of threads: 2 (available to the VM)
- Clock: 2.30 GHz (turbo 3.70 GHz)
- Cache: 24.75 MB L3 cache (for whole chip)
- Memory type: DDR4
- Memory size: ~2 GB (available to the VM)

Skylake specs reported by [Anandtech](https://www.anandtech.com/show/11544/intel-skylake-ep-vs-amd-epyc-7000-cpu-battle-of-the-decade/13)

- L1$: 4 cycles
- L2$: 768 KB per core, 14-22 cycles
- L3$: 1.375 MB per core, 54-56 cycles
- Memory: 89-91 cycles

## Amber's laptop 

Lenovo ideapad FLEX 5-1570

Intel ARK and reported specs:

* CPU: Intel Core i7-8550U (8th generation)
* Launch date: Q3'17
* Lithography: 14 nm
* Cores: 4
* Threads: 8
* Clock: 1.80 GHz, max 4.0 GHz 
* Cache: 8 MB Intel Smart Cache
* Memory type: DDR4
* Memory size: 16.0 GB
* Max memory bandwidth: 37.5 GB/s

