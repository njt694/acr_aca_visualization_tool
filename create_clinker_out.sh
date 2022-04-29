#! /usr/bin/env bash

# 3 shell scripts to run psiblasts, isolate psiblast information in tabdelimted format,
# and to create directories for each query (holding match data)

# Directory to save the psi-blast results
cd /birl2/data/Acr/clean/psiblast_out

# run the psi-blasts
sh /birl2/data/Acr/clean/scripts/run_psiblasts.sh /birl2/data/Acr/data/updateddb /birl2/data/Acr/clean/fastagenes

# Move to clinker dir so that master gene match file is correctly modified
cd /birl2/data/Acr/clean/scripts/clinker

# script to parse psiblast outs
for FILE in /birl2/data/Acr/clean/psiblast_out/*.all.out
do
        python ../parse_psiblast_out.py $FILE > /birl2/data/Acr/clean/tabdelimitedouts_bacterial/$(basename $FILE).parsed
done

#sh run_find_genomes.sh       No longer useful, parse_psiblast_outs.py does this and more

sh ../set_directories_matches.sh

# change directory to wherever the formated tab delimited psibalst outputs are stored
cd /birl2/data/Acr/clean/tabdelimitedouts_bacterial

# loop through and create the genbank files (see parse_genbank_file.py for output location specifics)
# Ensure that the BLASTDB path is set to the specific database location
for query in *.parsed
do
        python3 ../scripts/parse_genbank_file.py $query

done

# Visualize taxonomy (pies and trees)
sh /birl2/data/Acr/clean/scripts/phylo_pipe.sh /birl2/data/Acr/clean/directory_of_genbank_matches_bacterial

# Running clinker through pipe not tested
# For each clinker script, cd to scripts/clinker (where the master file is stored) and run main.py instead of clinker:
# python main.py /birl2/data/Acr/clean/directory_of_genbank_matches_bacterial/dir_you_want_plot_of/*.gb -p outfilename.html
# Implement a loop to work for all acrs all at once