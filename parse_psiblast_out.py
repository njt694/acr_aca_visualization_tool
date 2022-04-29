#! /usr/bin/env python
"""
File used to prune redundant (duplicates within same genome) psi-BLAST matches and reformat the output to be used by
future files in the pipeline. It outputs the newly formatted matches to stdout and also modifies the master match file
(must specify directory, within the clinker directory). As well as generating a separate file with all match names
specific to the Acr in question.
"""


from sys import stdout, argv
from Bio import SeqIO

filename = argv[1]
f = open(filename, 'r')
lines = [line.rstrip() for line in f]
f.close()


match_info = [line.split()[1] for line in lines]
e_values = [line.split()[-1].rstrip() for line in lines]


genes = {}
for i in range(len(match_info)):
    match = match_info[i].split("|")
    gca_accession = match[0]
    genome_accession = match[1]
    gene_accession = match[2]
    e_value = e_values[i]
    start = match[4]
    stop = match[5]

    if gene_accession not in genes.keys():
        genes[gene_accession] = {"gca": [gca_accession], "genome": [genome_accession], "eval": [e_value], "start": [start], "stop": [stop]}
    else:
        genes[gene_accession]["gca"].append(gca_accession)
        genes[gene_accession]["genome"].append(genome_accession)
        genes[gene_accession]["eval"].append(e_value)
        genes[gene_accession]["start"].append(start)
        genes[gene_accession]["stop"].append(stop)


duplicates = []
non_redundants = []

for gene in genes.keys():
    if len(genes[gene]["genome"]) > 1:
        duplicates.append(gene)
    else:
        non_redundants.append([genes[gene]["gca"][0], gene, genes[gene]["eval"][0], genes[gene]["start"][0], genes[gene]["stop"][0]])

for gene in duplicates:
    record = genes[gene]
    genomes = record["genome"].copy()

    genome_index_pair = []
    dupes = []
    for i in range(len(genomes)):
        genome_index_pair.append((i, genomes[i]))

    temp = []
    count = 0
    for genome in genomes:
        if genome not in temp:
            count += 1
            temp.append(genome)

    for i in range(count):

        potential_dupe = genome_index_pair[0]
        match_temp = [genome_index_pair[0]]

        for pair in genome_index_pair[1:]:
            if pair[1] == match_temp[0][1]:
                match_temp.append(pair)

        genome_index_pair = [pair for pair in genome_index_pair if pair[1] != potential_dupe[1]]
        dupes.append(match_temp)

    # Now match_temp = [[(index, genome1), (index, genome1)], [(index, genome2)]]

    for duplicated_genome_list in dupes:
        # Keep pair with the lowest e-value
        if len(duplicated_genome_list) > 1:
            lowest = None
            for pair in duplicated_genome_list:
                pair_eval = genes[gene]["eval"][pair[0]]
                if lowest is None:
                    lowest = pair_eval
                else:
                    try:
                        # lowest is in form #e#
                        lowest_split_eval = lowest.split('e')
                        lowest_decimal = lowest_split_eval[0]
                        lowest_exponent = lowest_split_eval[1]
                    except:
                        # lowest is in form 0.004
                        lowest_decimal = float(lowest) * 1000
                        lowest_exponent = 0
                    try:
                        # pair eval in form #e#
                        split_pair_eval = pair_eval.split('e')
                        pair_decimal = split_pair_eval[0]
                        pair_exponent = split_pair_eval[1]
                    except:
                        # pair eval in form 0.001
                        pair_decimal = float(pair_eval) * 1000
                        pair_exponent = 0

                    if int(pair_exponent) < int(lowest_exponent):
                        lowest = pair_eval
                    elif int(pair_exponent) == int(lowest_exponent):
                        if float(pair_decimal) < float(lowest_decimal):
                            lowest = pair_eval

            lowest_eval_index = genes[gene]["eval"].index(lowest)
        else:
            lowest_eval_index = 0
        non_redundants.append([genes[gene]["gca"][lowest_eval_index], gene, genes[gene]["eval"][lowest_eval_index], genes[gene]["start"][lowest_eval_index], genes[gene]["stop"][lowest_eval_index]])

# Write all the non-redundant genes/genomes to stdout
for line in non_redundants:
    writeString = ""
    for item in line:
        writeString += item + '\t'
    writeString += '\n'
    stdout.write(writeString)

# Write all the gene matches to a file to be used for clinker labeling
query_name = filename.split('.')[0].split('/')[-1]

f = open(query_name+"_match_names.txt", "w")
text = ""
for line in non_redundants:
    text += line[1] + '\t' + query_name + '\n'
f.write(text.rstrip())
f.close()

# Modify master file
try:
    # all_match_names.txt exists
    f = open("all_match_names.txt", "r")
    existing_lines = [line.rstrip().split() for line in f]
    f.close()
except:
    # all_match_names.txt doesn't exist
    existing_lines = []

existing_matches = [line[0] for line in existing_lines]

for line in non_redundants:
    if line[1] not in existing_matches:
        existing_lines.append([line[1], query_name])
    else:
        # Protein acc. already in the master file from another Acr
        pass

all_str = ""
for line in existing_lines:
    all_str += line[0] + '\t' + line[1] + '\n'

f = open("all_match_names.txt", "w")
f.write(all_str)
f.close()
