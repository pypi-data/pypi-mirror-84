#!/usr/bin/env python

import argparse
import os.path
import sys

def build_genes_set(genes_file, to_upper = True):
    """Returns a set of genes from a simple file with a gene in every row

    Parameters:

    genes_file (string): the file containing one gene per line
    to_upper (boolean): return all uppercase gene names


    Returns:
    set: The set of all genes in the parsed file
    """

    if os.path.isfile(genes_file) == False:
        print("{} do not exists".format(genes_file), file=sys.stderr)
        return -1

    genes = []

    with open(genes_file) as genes_file:
        for line in genes_file.readlines():
            splitted_line = line.split()
            gene = splitted_line[0]
            if to_upper == True:
                gene = gene.upper()
            genes.append(gene)

    genes = set(genes)
    return genes

def get_genes_from_info(info):
    """Gets the gene names from the INFO columns of a VCF

    Parameters:

    info (string): the INFO field from a VCF variant line


    Returns:
    list: The list of the genes present in the INFO field
    """

    genes = []
    splitted_info = info.split(";")
    for element in splitted_info:
        if element.startswith("ANN="):
            mutations = element.split(",")
            for mutation in mutations:
                splitted_mutation = mutation.split("|")
                gene = splitted_mutation[3]
                genes.append(gene)
    return genes

def main():
    parser = argparse.ArgumentParser(description="Filter a vcf by gene names")
    parser.add_argument('-g', '--genes', action='store', type=str, help="A file with one gene name per line", required=True)
    parser.add_argument('-v', '--vcf', action='store', type=str, help="The VCF to be filtered", required=True)
    parser.add_argument('-m', '--meta', action='store', type=str, help="Show or not show meta-information", required=False, default="T")
    parser.add_argument('-t', '--throw', action='store', type=str, help="Throw away genes present in the file indicated by -g", required=False, default="F")
    args = parser.parse_args()

    genes = args.genes
    vcf = args.vcf
    meta = args.meta
    throw = args.throw

    genes_to_keep_or_trash = build_genes_set(genes)
    
    with open(vcf) as vcf:
        for line in vcf.readlines():
            if line.startswith("#"):
                if meta == "T":
                    print(line[:-1])
                else:
                    pass
            else:
                splitted_line = line.split()
                if len(splitted_line) < 7:
                    pass
                else:
                    info = splitted_line[7]
                    genes = get_genes_from_info(info)
                    for gene in genes:
                        gene = gene.upper()
                        if throw == "F":
                            if gene in genes_to_keep_or_trash:
                                print(line[:-1])
                                break
                        else:
                            if gene not in genes_to_keep_or_trash:
                                print(line[:-1])
                                break
    return 1

if  __name__ == "__main__":
    main()

