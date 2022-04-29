#!/usr/bin/env python3

import argparse
from os import listdir
from os.path import isfile, join
import gzip
import re

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--organism", type=str, help="organism to limit protein FASTA file to", default=None)
parser.add_argument("gbff_dir", type=str, help="Directory containing GBFF files")

args = parser.parse_args()

onlyfiles = [f for f in listdir(args.gbff_dir) if isfile(join(args.gbff_dir, f))]

i = 1

for gbff_filename in onlyfiles:

    if ".gbff.gz" not in gbff_filename:
        continue

    #print("(" + str(i) + ") " + gbff_filename)
    i += 1
    infile = gzip.open(gbff_filename, mode="rt")
    try:
        file_contents = infile.read()
    except:
        print("Error reading gz file " + gbff_filename)
        continue
    infile.close()


    organism_OK = True
    if args.organism:
        organism_OK = False
        for line in file_contents.split("\n"):
            if " ORGANISM" in line:
                if args.organism in line:
                    organism_OK = True
                    break

    if not organism_OK:
        continue

    loci = file_contents.split("LOCUS       ")[1:]

    for item in loci:
        exclude_origin_from_split = re.search(r'(.+?)ORIGIN.*', item, re.DOTALL)
        item = exclude_origin_from_split.group(1)
        accession = item.split(" ")[0]
        CDSs = item.split("\n     CDS")[1:]

        for CDS in CDSs:
            exclude_gene_from_split = re.search(r'(.+?)gene            .*', CDS, re.DOTALL)

            if exclude_gene_from_split:
                CDS = exclude_gene_from_split.group(1)

            position_regexp = re.search(r'complement\((\d+\.\.\d+)\)', CDS)

            if position_regexp:
                complement = True
                position = position_regexp.group(1)
            else:
                position_regexp = re.search(r'([<>\d]+\.\.[<>\d]+)', CDS)
                if position_regexp:
                    position = position_regexp.group(1)
                else:
                    position = "?..?"

            start,stop = position.split("..")
            start = start.replace(">", "")
            start = start.replace("<", "")
            stop  = stop.replace(">", "")
            stop  = stop.replace("<", "")

            gene_regexp = re.search(r'/gene="(.+?)"', CDS)

            if gene_regexp:
                gene = gene_regexp.group(1)
            else:
                gene = "?"

            locus_tag_regexp = re.search(r'/locus_tag="(.+?)"', CDS)

            if locus_tag_regexp:
                locus_tag = locus_tag_regexp.group(1)
            else:
                locus_tag = "?"

            product_regexp = re.search(r'/product="(.+?)"', CDS, re.DOTALL)
            #product_regexp = re.search(r'/product="(.+?)"', CDS)

            if product_regexp:
                product = product_regexp.group(1)
                product = product.replace("\n", "")
                product = re.sub(" {2,}", " ", product)
            else:
                product = "?"

            proteinID_regexp = re.search(r'/protein_id="(.+?)"', CDS)

            if proteinID_regexp:
                proteinID = proteinID_regexp.group(1)
            else:
                proteinID = "?"

            db_xref_regexp = re.search(r'/db_xref="(.+?)"', CDS)

            if db_xref_regexp:
                db_xref = db_xref_regexp.group(1)
            else:
                db_xref = "?"

            translation_regexp = re.search(r'/translation="(.+?)"', CDS, re.DOTALL)

            if translation_regexp:
                translation = translation_regexp.group(1)
                translation = translation.replace(" ", "")
                translation = translation.replace("\n", "")
            else:
                translation = "?"

            if translation != "?":
                print(">{}|{}|{}|{}|{}|{}|{}\n{}".format(gbff_filename, accession, proteinID, gene, start, stop, product, translation))