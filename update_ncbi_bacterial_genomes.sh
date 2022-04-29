#!/usr/bin/env bash

# Script to update/build the ncbi bacterial database

echo "Building new_genomes_urls.txt..."
get_list_of_new_ncbi_bacterial_genomes.py | grep -v 'na/na' | sort | uniq > new_genomes_urls.txt
echo "Finding broken genomes urls..."
get_list_of_new_ncbi_bacterial_genomes_na.py | grep 'na/na' | sort | uniq > broken_new_genomes_urls.txt


mkdir new_genomes_$$
cd new_genomes_$$

for url in `cat ../new_genomes_urls.txt`; do bn=`basename $url`; if [ ! -e $bn ]; then echo "Downloading URL $url"; wget -t 1 --timeout=5 $url; else echo "Already downloaded $url"; fi; done
echo "Finished Downloading New Genomes"

# Check for missing genomes
for genome in $(cat ../new_genomes_urls.txt | cut -d "/" -f 11 | sort | uniq); do if [ ! -e $genome ]; then echo $genome; fi; done

# Check for messed-up GBFF files
# If there are some, they need to be re-downloaded.
# This needs to be done before creating the locus map, otherwise it will give an error.
# I am fairly certain this does nothing
check_gbff.gz_files.py . > ../messed_up_gbff_files.txt

#make_gbff_protein_fasta.py . > ../new_proteins.FASTA
#cat ../new_proteins.FASTA >> /birl2/data/Acr/data/bacterial_genomes/protein/all_proteins.FASTA
#rm ../new_proteins.FASTA
#for thing in `find . -name "*.gbff.gz"`; do mv $thing /birl2/data/Acr/data/bacterial_genomes/gbff; done

#cd /birl2/data/Acr/data/bacterial_genomes/protein
#makeblastdb -in /birl2/data/Acr/data/bacterial_genomes/protein/all_proteins.FASTA -dbtype prot

#mv all_proteins.FASTA.* /birl2/data/Acr/data/blastdb
