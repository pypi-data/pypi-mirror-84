import setuptools


#scripts=['change_set_subfield'] ,

setuptools.setup(
     name='iSeqs2',  
     version='0.0.3',
     author="Alessandro Coppe",
     author_email="",
     description="Another bunch of scripts I use in my Next Generation Sequencing Bioinformatics Analyses",
     url="https://github.com/alexcoppe/iSeqs2",
     packages=["iseqs2"],
     scripts=["scripts/build_leukemia_genes_list/build_leukemia_genes_list.py",
         "scripts/filter_by_normal_expression/filter_by_normal_expression.py",
         "scripts/filter_strelka2/filter_strelka2.py",
         "scripts/remove_snps_from_cosmic/remove_snps_from_cosmic.py",
         "scripts/filter_vcf_by_gene_names/filter_vcf_by_gene_names.py",
         "scripts/filter_varscan2_vcfs/filter_varscan2_vcfs.py",
         "scripts/remove_germline_variants_from_varscan/remove_germline_variants_from_varscan.py",
         "scripts/nucleotides_frequency_from_bam_positions/nucleotides_frequency_from_bam_positions.py",
         "scripts/join_tables_from_snpsift_extractFields/join_tables_from_snpsift_extractFields.py"],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
)
