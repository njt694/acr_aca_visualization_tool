#! /usr/bin/env python
"""
Script to count the number of Acr/Aca genes in a given genbank file. Records number and names of the Acas/Acrs.
Writes lines that can be save to a .csv to stdout.

May need to modify path_to_master_file (line 11)
"""

from Bio import SeqIO
from sys import argv, stdout

path_to_master_file = '/birl2/data/Acr/clean/scripts/clinker/'
master_file = path_to_master_file + 'all_match_names.txt'

f = open(master_file, 'r')
lines = [line.rstrip().split() for line in f]
f.close()

genes = []

for seq_record in SeqIO.parse(argv[1], 'genbank'):
    try:
        accession = seq_record.annotations['accessions'][0] + '.' + str(seq_record.annotations['sequence_version'])
    except KeyError:
        try:
            accession = seq_record.annotations['accessions'][0]
        except KeyError:
            accession = 'null'
    for feature in seq_record.features:
        if 'protein_id' in feature.qualifiers.keys():
            genes.append(feature.qualifiers["protein_id"][0])

counter = 0
out = []
for i in range(len(lines)):
    if lines[i][0] in genes:
        counter += 1
        pair = lines[i][0] + ';' + lines[i][1]
        out.append(pair)

outstr = accession + ',' + argv[1].split('/')[-1] + ',' + str(counter)
for o in out:
    outstr += ',' + o

stdout.write(outstr+'\n')
