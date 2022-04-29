#!/usr/bin/env python3

# This file was used to download the bacterial genomes from the NCBI website
# Only outputs files that are recognized as files

import urllib.request
import os.path
import os

response = urllib.request.urlopen("ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt")
data = response.read()
text = data.decode("utf-8")

lines = text.split("\n")

lines = lines[2:-1]

for i in range(len(lines)):
    line = lines[i].rstrip()
    organism = line.split("\t")[7]
    #dl_directory = line.split("\t")[19]
    #"""
    try:
        dl_directory = line.split("\t")[19]
    except IndexError:
        string = ""
        for item in line:
            string += str(item)
            string += "\t"
        string += "BIGERROR"
        print(string)
    #"""
    organism = organism.replace(" ", "_")
    dl_name = dl_directory.split("/")[-1]

    filename =  dl_name + "_genomic.gbff.gz"

    url = dl_directory + "/" + filename

    #potentially_existing_filename = os.environ["HOME"] + "/NCBI/bacterial_genomes/gbff/" + filename
    potentially_existing_filename = "/birl2/data/Acr/data/bacterial_genomes/gbff/" + filename

    if os.path.isfile(potentially_existing_filename):
        #pass
        print(url)
        #print(url + "\t" + str(i) + "\t" + lines[i])