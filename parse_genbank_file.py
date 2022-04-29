#! /usr/bin/env python
"""
Program used to isolate the gene clusters of the psiblast matches of Acr/Aca proteins. Can add a command-line arg to
modify the n param in find_cluster()
"""

from Bio import SeqIO
import sys
import fileinput
import gzip

filein = fileinput.input()

lines = [line for line in filein]

# holds the column values from a modified tab delimted psiblast output for each match against a query
genomes = []
accessions = []
e_values = []

# go through each line (match) of the formatted psiblast output and add their values into the corresponding lists
# each element position regards to a specific match across all lists (aka element [0] is 1 match for 3 lists, just holding different data)
for line in lines:

    if line.split()[1] in accessions:
        match_already_present_index = accessions.index(line.split()[1])

        if e_values[match_already_present_index] > float(line.split()[2]):
            genomes[match_already_present_index] = line.split()[0]
            accessions[match_already_present_index] = line.split()[1]
            e_values[match_already_present_index] = float(line.split()[2])

    else:
        genomes.append(line.split()[0])
        accessions.append(line.split()[1])
        e_values.append(float(line.split()[2]))


def find_cluster(genomename, accessionpos, n=20):
    """
    Function to find the clusters of a psiblast match and return the cluster a certain number up and downstream
    from the match found
    Param: genomename = Genome to look through
    Param: accessionpos = accession of the psiblast match
    Return: Genbank Record containing a certain number
    """
    # the path for opening the file must point to the directory holding genomes (.gbff.gz files)
    with gzip.open("/birl2/data/Acr/data/bacterial_genomes/gbff/" + genomename, "rt") as openedgenome:
        recordlist = SeqIO.parse(openedgenome, "gb")

        # user the parser to parse through the genbank record and the features of each record
        for record in recordlist:
            # two lists hold the features n upstream and downstream of the match in record
            n_upstream_plusmatch = []
            n_downstream = []
            matchreached = False

            for feature in record.features:

                if feature.type == "CDS":

                    # if the match is not found in record, and the list is not at 20 capacity, then add to upstream list
                    if matchreached == False:
                        if len(n_upstream_plusmatch) < n + 1:
                            n_upstream_plusmatch.append(feature)


                        # else remove the oldest feature from the list and add the new one (maintain n upstream from match)
                        else:
                            n_upstream_plusmatch.pop(0)
                            n_upstream_plusmatch.append(feature)

                    # match is found, begin adding to downstream list
                    else:

                        if len(n_downstream) < n:
                            n_downstream.append(feature)
                            if feature == record.features[-1]:
                                print(
                                    "TRUE Reached end of record")  # output indicating end of record (no more downstream genes in record)
                                n_upstream_plusmatch.extend(n_downstream)  # combine the two lists into one
                                gene_cluster = record_match_foundin[(n_upstream_plusmatch[0].location.start): (
                                    n_upstream_plusmatch[-1].location.end)]
                                return gene_cluster


                        # twenty is in downstream list, create genbank cluster and return
                        else:
                            n_upstream_plusmatch.extend(n_downstream)
                            gene_cluster = record_match_foundin[(n_upstream_plusmatch[0].location.start): (
                                n_upstream_plusmatch[-1].location.end)]
                            return gene_cluster

                    # if a protein_id exists and it matches the accession number of the match
                    if 'protein_id' in feature.qualifiers and feature.qualifiers['protein_id'][0] == accessionpos:
                        record_match_foundin = record
                        # print(record_match_foundin.id)          # indicates the record number the match was found in (uncomment if you want this output)
                        matchreached = True  # indicates taht the match has been found

                        # if the match is the last feature in the record, return the cluster
                        if feature == record.features[-1]:
                            n_upstream_plusmatch.extend(n_downstream)
                            gene_cluster = record_match_foundin[(n_upstream_plusmatch[0].location.start): (
                                n_upstream_plusmatch[-1].location.end)]
                            print("Match in last Feature")
                            return gene_cluster

                elif feature.type != 'CDS' and feature == record.features[-1] and matchreached == True:
                    n_upstream_plusmatch.extend(n_downstream)  # combine the two lists into one
                    gene_cluster = record_match_foundin[
                                   (n_upstream_plusmatch[0].location.start): (n_upstream_plusmatch[-1].location.end)]
                    print("Match in last CDS")
                    return gene_cluster


def get_taxonomy(genomename):
    """
    Function to obtain the taxonmic information of each psiblast match from the delimited file input
    Param: genomename = Genome to look through (from the match)
    Return: List of Taxonomic information from the record the match was found in
    """
    # ensure that the directory is the correct specified location for the genome files
    with gzip.open("/birl2/data/Acr/data/bacterial_genomes/gbff/" + genomename, "rt") as openedgenome:
        recordlist = list(SeqIO.parse(openedgenome, "gb"))
        organism = recordlist[0].annotations['organism']
        recordlist[0].annotations['taxonomy'].append(organism)

        for each in range(len(recordlist[0].annotations['taxonomy'])):
            recordlist[0].annotations['taxonomy'][each] = recordlist[0].annotations['taxonomy'][each].replace(" ", "_")

        return recordlist[0].annotations['taxonomy']


print("Creating Clusters for " + fileinput.filename() + " as Input file...")

# list to hold the taxonomy of the matches so it can written to a file
taxonomy_of_matches = []

# for each genome in the tab delimited file of matchs, find the cluster create genbank file
for each in range(len(genomes)):
    Gene_cluster = find_cluster(genomes[each], accessions[each])
    genbankfile_matchname = Gene_cluster.description.replace(" ", "_").replace(":", "").replace(",", "")
    taxonomy_of_matches.append(get_taxonomy(genomes[each]))
    print(genbankfile_matchname)
    print(str(each) + " genome")

    # ensure that you write to the correct directory to hold the queries matches
    # or ensure the given filename is the direct path as done below
    SeqIO.write(Gene_cluster,
                "/birl2/data/Acr/clean/directory_of_genbank_matches_bacterial/" + fileinput.filename() + "/" + genbankfile_matchname.replace('/', '_') + '_' + str(
                    accessions[each]) + '_' + str(lines[each].split()[2]) + ".gb", "genbank")

print("------NEXT QUERY-------")

# creates the phylogeny tab delim'd file to be used to create visual output of match phylogeny (currently goes to same directory as the genbank clusters)
with open(
        "/birl2/data/Acr/clean/directory_of_genbank_matches_bacterial/" + fileinput.filename() + "/" + fileinput.filename() + "_taxonomy.txt",
        "w") as tax_file:
    tax_file.writelines("\t".join(i) + '\n' for i in taxonomy_of_matches)

filein.close()
