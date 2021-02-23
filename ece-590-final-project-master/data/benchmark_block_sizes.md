# Benchmark block sizes

This document lists how various tools report their results and how these results can be unified.
Remember that:

- 1 KB  =   1000 byte
- 1 MB  = 1000^2 byte
- 1 KiB =   1024 byte
- 1 MiB = 1024^2 byte

## Intel MLC

Intel MLC takes the block size argument in KB.
Our input block sizes are aligned to a multiple of 32 KB.
Block size is reported back in the output in MiB.
Latency results are reported in core clocks and nanoseconds.

*This information has been taken from the provided documentation.*

## Tinymembench

Tinymembench reports block size in byte.
Block sizes are aligned to a multiple of 1 KiB.
Latency results are reported in nanoseconds.
We are interested in the results labeled as "single random read, MADV_HUGEPAGE".

*This information has been taken from the output and source code of the program.*

## lmbench

lmbench reports block size in byte.
Block sizes are aligned to a multiple of 1 KiB.
Latency results are reported in nanoseconds.

*This information has been taken from the output and source code of the program.*

# Result unification

All tools report latency in nanoseconds, which is already a unified metric.
The block sizes of Intel MLC align to a KB while tinymembench and lmbench align to a KiB.
Because of this difference in alignment, Intel MLC might have a slight performance benefit over the other two benchmarks.
Though the difference for especially the small cache sizes will be negligible.

