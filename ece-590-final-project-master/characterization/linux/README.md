# Characterization tools

This directory collects the characterization tools for the cache and memory subsystem.
The tools in this directory are targeted at the Linux operating system.

Most directories contain a `run.sh` script to run the corresponding software.
To run all scripts, use the `run_all.sh` script.

## lmbench3

[lmbench website](http://www.bitmover.com/lmbench/)

lmbench3 is very old.
Last update in 2012, manual and website from 1998, archive looks like it is created in 2005.

Compiles on Linux after [touching a missing file](https://github.com/zhanglongqi/linux-tips/blob/master/tools/benchmark.md).

```bash
cd lmbench3
mkdir ./SCCS
touch ./SCCS/s.ChangeSet
```

Compilation with optimized flags.

```bash
CFLAGS="-O2 -march=native -mtune=native"
make
```

Standard configuration using `make results` has a very long run time.
Over 4 hours runtime on Leon's laptop.
Resulting contains a lot of information we are not interested in.

There is a separate tool for benchmarking cache.
This tool can be used separately from the normal lmbench workflow.

```bash
./bin/x86_64-linux-gnu/cache
```

The `cache` tool does measure information of interest, including:

1. Cache size in byes and lines
1. Cache latencies
1. Cache parallelism (unknown metric)
1. Memory latency
1. Memory parallelism (unknown metric)

The `cache` tools has an edge detection algorithm to estimate the number of cache levels.
This algorithm is not always able to detect all cache levels properly.
The source file was modified to output more raw data for further manual inspection.

## tinymembench

[tinymembench website](https://github.com/ssvb/tinymembench)

Latest update in 2017.

Compiles and runs on Linux using the commands below.

```bash
cd tinymembench
CFLAGS="-O2 -march=native -mtune=native"
make
./tinymembench
```

Results include:

1. Memory bandwidth using various copy methods
1. Memory latency for various block sizes

## perf

[Linux perf home page](https://perf.wiki.kernel.org/index.php/Main_Page)

The Linux kernel tool `perf` is more a profiler than benchmarker.
At this moment, this tool will not be further investigated, but it might be useful later.
Other useful resources are listed below.

1. [Linux perf tutorial](https://perf.wiki.kernel.org/index.php/Tutorial)
1. [perf examples](http://www.brendangregg.com/perf.html)
1. [pmu-tools extension to perf](https://github.com/andikleen/pmu-tools)


## likwid

[likwid website](https://github.com/RRZE-HPC/likwid)

Performance toolsuite.
Includes a tool that reports the cache topology.
Not yet tested at this moment. It looks like the tool has limited use for us at this moment.

Compiles on Linux. Needs a build directory without whitespace in the address, otherwise the build fails.
Tool requires to be installed, hence `sudo` is required.

## valgrind and cachegrind

Valgrind and the associated tool cachegrind are promoted as cache profilers.
Hence they serve a similar purpose as `perf`.
At this moment, this tool will not be further investigated, but it might be useful later.
Useful resources are listed below.

1. [cachegrind manual](https://valgrind.org/docs/manual/cg-manual.html)
1. [cachegrind course material from Washington](https://courses.cs.washington.edu/courses/cse326/05wi/valgrind-doc/cg_main.html)

## memlatency

[memlatency website](https://github.com/SudarsunKannan/memlatency)

memlatency is a limited tool.
Compiles on Linux.
Crashes while running with the message `*** stack smashing detected ***`.

## latencies.c

[latencies.c gist](https://gist.github.com/Syntaf/f888032b0afd947e4b84)

This single file program is posted as an example to measure memory latencies.
The file does not build since it contains errors.
Comments also suggest that the program contains a segfault.
This tool is not further investigated.

## Intel Memory Latency Checker

[Intel MLC website](https://software.intel.com/en-us/articles/intelr-memory-latency-checker)

Intel Memory Latency Checker can only be downloaded through the website if the user agrees to the terms.
This tool provides binaries for both Linux and Windows.

The tool is intended for multi-socket systems with non-uniform memory access.
The tool is closed source and according to the manual it requires `sudo` to run.
Without `sudo`, the program works without modifying prefetchers and uses random access for latency measurements.

Reported results include:

1. Peak injection memory bandwidth (unknown metric)
1. Loaded memory latencies (unknown metric)
1. A few other unknown metrics

At this moment, it is not clear if the results of this tool are useful for us.

