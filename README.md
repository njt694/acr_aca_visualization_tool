# acr_aca_visualization_tool
A tool to visualize the genomic neighbourhoods and phylogeny of anti-CRISPR and anti-CRISPR associated genes.

Running create_clinker_out.sh will generate everything except co_occurrence data and clinker plots, those must be
generated separately. A description on how to generate clinker plots is found in create_clinker_out.sh.

The following scripts contain hard-coded directories and will need to be modified, or the directory hierarchy that the
scripts were designed on will need to be mimicked. I may have missed some of the hard-coded paths, so if you get an
error, that is likely the cause.

Scripts with hard-coded paths:
    co_occurrences.py
    create_clinker_out.sh
    db_phylogeny.py
    get_list_of_new_ncbi_bacterial_genomes_na.py
    get_list_of_new_ncbi_bacterial_genomes.py
    parse_genbank_file.py
    parse_psiblast_out.py
    run_psiblasts.sh
    set_directories_matches.sh
    update_ncbi_bacterial_genomes.sh


Original File Hierarchy (the files provided make up the contents of /birl2/data/Acr/clean/scripts/ )
    /birl2/data/Acr
        /clean/
            cooccurrences/
            directory_of_genbank_matches_bacterial/
            fastagenes/
            psiblast_out/
            scripts/
                basictree.py
                build_phylo.py
                clinker/
                    all_match_names.txt
                    align.py
                    classes.py
                    disjoint_set/
                    examples/
                    formatters.py
                    __init__.py
                    main.py
                    plot/
                        clinker.js
                        clustermap.min.js
                        d3.min.js
                        index.html
                        mock.json
                        style.css
                    plot.py
                co_occurrences.py
                create_clinker_out.sh
                db_phylogeny.py
                get_list_of_new_ncbi_bacterial_genomes_na.py
                get_list_of_new_ncbi_bacterial_genomes.py
                parse_genbank_file.py
                parse_psiblast_out.py
                phylo_pipe.sh
                run_cooccurrences.sh
                run_find_genomes.sh
                run_psiblasts.sh
                set_directories_matches.sh
                split_pal.py
                split_query_name.py
                update_ncbi_bacterial_genomes.sh
            tabdelimitedouts_bacterial/
        /data
            /updateddb
                all_pal_names.txt
                db_volume_files.....
            /bacterial_genomes
                /gbff
                    all.gbff
                    files.gbff
                    in.gbff
                    the.gbff
                    database.gbff
                    
                   
Uses modified code from Clinker:
clinker & clustermap.js: Automatic generation of gene cluster comparison figures.
Gilchrist, C.L.M., Chooi, Y.-H., 2020.
Bioinformatics. doi: https://doi.org/10.1093/bioinformatics/btab007

The python library disjoint-set will need to be installed for clinker to run properly. This can be done from the command line with: 
pip install disjoint-set
