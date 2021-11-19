#!/bin/sh
# This script extracts the NYT and time.com sections from a given jsonl.gz file
# That is, it creates two new files $1.time.jsonl and $1.nyt.jsonl

zgrep -aE 'https?:\\/\\/www\.nytimes\.com\\/' "$1" > "$1.nyt.jsonl"
zgrep -aE 'https?:\\/\\/(www\.)?time\.com\\/' "$1" > "$1.time.jsonl"

