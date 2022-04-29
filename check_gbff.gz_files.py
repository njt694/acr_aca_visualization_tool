#!/usr/bin/env python3

import argparse
from os import listdir
from os.path import isfile, join
import gzip


description='''
WHEN RUNNING THIS SCRIPT YOU SHOULD BE IN THE gbff directory and it should be run as create_locus_map.py ~/data/bacterial_genomes/gbff > locus_to_filename_map.txt
*** THIS SHOULD ONLY NEED TO BE RUN ONCE. IT WAS USED TO CREATE THE FILE locus_to_filename_map.txt ***
Given a .gbff file as input, it scans the file for a LOCUS line,
then parses out the LOCUS accession number, and then outputs a mapping between the accession
number and the filename. This is used so that when the bacterial database is BLASTed against,
it is possible to tell quicly which filename a given match came from.

Note from subsequent programmer. I'm not sure if this script actually does anything, I've modified it to perform what I
think was its original purpose (to try and find gbff.gz files that don't open).
'''

parser = argparse.ArgumentParser(description=description,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("dir", type=str, help="gbff directory")
args = parser.parse_args()

onlyfiles = [f for f in listdir(args.dir) if isfile(join(args.dir, f))]

i = 1
for gbff_filename in onlyfiles:

    if ".gbff.gz" not in gbff_filename:
        continue

    #print("(" + str(i) + ") " + gbff_filename)
    i += 1
    file = gzip.open(gbff_filename, mode="rt")

    try:
        first_line = file.readline()
    except:
        print("Error reading gz file " + gbff_filename)
        continue