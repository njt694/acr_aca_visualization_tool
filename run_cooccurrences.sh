#! /usr/bin/env bash
# Script to run python script which counts co-occurrences of Acr/Aca genes that have been PSI-BLASTEd. Designed to run
# on the directory of genbank files created by parse_genbank_file.py.
# Run as: sh run_cooccurrences.sh /path/to/genbank_file_directory

touch $(basename $1)_cooccurrences.txt
for FILE in $1/*.gb
do
  python $1/../../scripts/co_occurrences.py $FILE >> $(basename $1)_cooccurrences.txt
done
