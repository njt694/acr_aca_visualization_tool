#! /usr/bin/env python

from sys import stdin, stdout, stderr

lines = [line for line in stdin]

if lines[0][0] != '>':
    stderr.write("Error reading query. First line of fasta does not contain '>'.")

query_name = lines[0].split()[0]
query_name = query_name[1:]

stdout.write(query_name)
