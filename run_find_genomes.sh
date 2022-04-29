#! /usr/bin/env bash
# Deprecated. Replaced by parse_psiblast_out.py

# script to produce tab delimeted output of the psiblast matches output.
# This includes: Genomename from database
# redirects to specified directory
for file in /birl2/data/Acr/clean/psiblast_out/*.out
do
        awk -F '\t' '{print $2"|"$12}' $file | awk -F '|' '{print $1"\t"$3"\t"$8"\t"$5"\t"$6}' | head -n -2 > /birl2/data/Acr/clean/tabdelimitedouts_bacterial/$(basename "$file").delimited

done

