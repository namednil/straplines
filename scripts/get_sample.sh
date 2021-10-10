#/bin/bash
# Takes a sample from the given gzip file from the first 100_000 lines.
gzip -cdfq $1 | head -100000 | shuf

