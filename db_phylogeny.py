#! /usr/bin/env python
"""
Program used to get the phylogenetic distribution of the database.

Doesn't work correctly for unknown reasons.
This script is a modified version of parse_genbank_file.py designed to run on all the .gbff files in the database to
generate a taxonomy file for the entire database.
"""

from Bio import SeqIO
from sys import argv
import gzip
import os

gbff_folder = "/birl2/data/Acr/data/bacterial_genomes/gbff"

# Directory containing gbff genomes
directory = argv[1]

filenames = []

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        filenames.append(f)

err_files = []

def get_taxonomy(genomename):
    """
    Function to obtain the taxonmic information of each psiblast match from the delimited file input
    Param: genomename = Genome to look through (from the match)
    Return: List of Taxonomic information from the record the match was found in
    """
    # ensure that the directory is the correct specified location for the genome files
    try:
        with gzip.open(genomename, "rt") as openedgenome:
            recordlist = list(SeqIO.parse(openedgenome, "gb"))
            organism = recordlist[0].annotations['organism']
            recordlist[0].annotations['taxonomy'].append(organism)

            for each in range(len(recordlist[0].annotations['taxonomy'])):
                recordlist[0].annotations['taxonomy'][each] = recordlist[0].annotations['taxonomy'][each].replace(" ","_")

            return recordlist[0].annotations['taxonomy']
    except:
        print("Error opening file "+genomename)
        err_files.append(genomename)


# list to hold the taxonomy of the genomes so it can written to a file
taxonomy_of_genomes = []

for each in range(len(filenames)):
    taxonomy_of_genomes.append(get_taxonomy(filenames[each]))

lines = ""
for i in taxonomy_of_genomes:
    try:
        linestr = "\t".join(i) + '\n'
        lines += linestr
    except:
        print("Error with line " + i)



with open('./all_gbff_taxonomy.txt', 'w') as tax_file:
    tax_file.write(linestr)

with open('./error_gbffs.txt', 'w') as err_file:
    err_file.writelines(gbff + '\n' for gbff in err_files)
