#!/usr/bin/env bash
# Pipe used to run all phylogeny-visualization scripts.
# Call as: sh phylo_pipe.sh /directory_of_genbank_matches_bacterial

#for dirr in $1/*
#do
#       mkdir $dirr/phylo_visualization
#done


for dir in $1/*
do
        echo Directory: $dir
        echo Taxonomy File Length:
        cat $dir/*taxonomy.txt | wc -l

        ls $dir | wc -l

        #cd $dir/phylo_visualization

        #pwd
        #echo Building Phylogenetic Tree...
        #python ../../../scripts/build_phylo.py ../*taxonomy.txt
        #echo Making Taxonomic Pie Charts...
        #python ../../../scripts/make_pie.py ../*taxonomy.txt 1 2 3 4 5 6 7
        echo --------------------------------------------------------------
        echo
done