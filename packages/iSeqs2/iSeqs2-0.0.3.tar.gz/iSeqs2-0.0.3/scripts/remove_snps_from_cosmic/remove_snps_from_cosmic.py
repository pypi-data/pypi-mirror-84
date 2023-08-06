#!/usr/bin/env python

import argparse
import os.path
import sys
import gzip
import re


def snps_from_cosmic(cosmic_file):
    """
    Returns a set of SNPs from COSMIC

    Parameters:

    cosmic_file (string): the file path to the COSMIC data (example: CosmicCodingMuts.vcf.gz)


    Returns:
    set: The set of all cosmic IDs that are a SNP
    """

    cosmic_snps = []
    with gzip.open(cosmic_file, 'rb') as f:
        for line in f:
            line = line.decode('ascii')
            if not line.startswith("#"):
                splitted_line = line.split()
                cosmic_id = splitted_line[2]
                info = splitted_line[-1]
                splitted_info = info.split(";")
                for splitted_info_point in splitted_info:
                    if splitted_info_point == "SNP":
                        cosmic_snps.append(cosmic_id)
                        break
    return set(cosmic_snps)


def get_cosmic_ids(vcf_line):
    '''
    Get the COSMIC id from the VCF's info field 

    Parameters:

    vcf_line (string): a line from a VCF file

    Returns:

    A list of COSMIC ids
    '''
    cosmic_ids = []
    splitted_line = vcf_line.split("\t")
    info_field = splitted_line[7]
    p = re.compile("COSM\d+")
    m = p.finditer(info_field)
    for match in m:
        span = match.span()
        cosmic_id = info_field[span[0]:span[1]]
        if cosmic_id != None:
            cosmic_ids.append(cosmic_id)
    cosmic_ids = list(set(cosmic_ids))
    return cosmic_ids


def main():
    parser = argparse.ArgumentParser(description="Removes the SNPs from COSMIC")
    parser.add_argument('-c', '--cosmic', action='store', type=str, help="The file from Cosmic (Example: CosmicCodingMuts.vcf.gz)", required=True)
    parser.add_argument('-v', '--vcf', action='store', type=str, help="The VCF to be filtered by SNPs from COSMIC", required=True)
    args = parser.parse_args()

    cosmic_snps = snps_from_cosmic(args.cosmic)

    is_snp = False
    with open(args.vcf) as vcf:
        for line in vcf:
            if line.startswith("#"):
                print(line[:-1])
            else:
                cosmic_ids = get_cosmic_ids(line)
                if len(cosmic_ids) == 0:
                    print(line[:-1])
                else:
                    is_snp = False
                    for cosmic_id in cosmic_ids:
                        if cosmic_id in cosmic_snps:
                            is_snp = True
                    if is_snp == False:
                        print(line[:-1])
                    is_snp = False

if  __name__ == "__main__":
    main()
