#! /usr/bin/env bash
# This script must specify the directory in which the fasta queries are located
# as well, the BLASTDB blast variable must point to the location of the database you wish to blast against
# Run as ./run_psiblasts /path/to/database/directory /path/to/fasta/query/files/directory
# In the directory you want the psiBLAST outputs to be in

DBDIR=$1
FASTADIR=$2

for file in "$FASTADIR"/*.fasta
do
        echo Psiblast Query: $file
        QUERY_NAME=$(/birl2/data/Acr/clean/scripts/split_query_name.py < $file)
        #declare -i COUNTER=0
        while read db_name;
        do
                echo Querying: $db_name
                psiblast -query "$file" -db "$DBDIR/$db_name" -num_iterations 4 -num_threads 4 -outfmt "6 qacc sacc pident qcovhsp length mismatch gapopen qstart qend sstart send evalue"  -evalue 0.01 -out "$(basename $file).out"
                cat $(basename $file).out | grep $QUERY_NAME >> $(basename $file).all.out
                #COUNTER=$((COUNTER+1))
        done < $DBDIR/all_pal_names.txt
done