#! /usr/bin/env bash

# script to obtain all the psiblast outputs, make directories for their genbank matches
# specify the directory where the delimited psiblast outputs are, and the directory in which to store
# the directories of matchs (holding match information/genbank files)
# THIS formats it so that EACH query has a directory for all its matches and image data etc.
for protein in /birl2/data/Acr/clean/tabdelimitedouts_bacterial/*.parsed
do
        mkdir /birl2/data/Acr/clean/directory_of_genbank_matches_bacterial/$(basename "$protein")


done

