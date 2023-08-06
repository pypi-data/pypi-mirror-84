#!/usr/bin/env python

import argparse
import os.path
import sys
import zipfile

def find_expressed_variants(vcf, thpa_dictionary):
    vcf_exists = False
    vcf_exists = os.path.isfile(vcf)
    if vcf_exists == False:
        print("File {} do not exists".format(vcf))
        sys.exit(1)

    with open(vcf) as vcf_content:
        for line in vcf_content.readlines():
            if line.startswith("#"):
                print(line[:-1])
            else:
                splitted_line = line.split("\t")
                info = splitted_line[7]
                splitted_info= info.split(";")
                for each_element in splitted_info:
                    if each_element.startswith("ANN="):
                        transcripts_info = each_element[4:]
                        splitted_transcript_info = transcripts_info.split(",")
                        for transcript in splitted_transcript_info:
                            splitted_transcript = transcript.split("|")
                            gene_id,ensg = splitted_transcript[3],splitted_transcript[4]
                            expression_value = thpa_dictionary.get(gene_id)
                            if expression_value != None:
                                print(line[:-1])
                                break
    return 0



def build_thpa_dictionary(normal_tissue_file_path, cell_types = ["B-cells", "NK-cells", "T-cells", "bone marrow", "dendritic cells", "granulocytes", "monocytes"], min_nx = 1):
    d = {}
    zfile = zipfile.ZipFile(normal_tissue_file_path)
    cell_types = set(cell_types)
    for finfo in zfile.infolist():
        if finfo.filename == 'rna_tissue_consensus.tsv':
            ifile = zfile.open(finfo)
            line_list = ifile.readlines()
            for line in line_list:
                line = str(line).replace("\\t", "\t")
                splitted_line = line.split("\t")
                tissue = splitted_line[2]
                nx = splitted_line[3]
                try:
                    nx = float(nx[:-3])
                except:
                    continue
                if tissue in cell_types and nx >= min_nx:
                    if not (splitted_line[1] in d):
                        d[splitted_line[1]] = [splitted_line[2]]
                    else:
                        d[splitted_line[1]].append(splitted_line[2])
    return(d)
    


def main():
    parser = argparse.ArgumentParser(description="Filter by rna_tissue_consensus.tsv.zip consensus transcript expression levels")
    parser.add_argument('-n', '--normal_tissue', action='store', type=str, help="rna_tissue_consensus.tsv.zip file path", required=True, default=None)
    parser.add_argument('-v', '--vcf', action='store', type=str, help="VCF to be filtered", required=True, default=None)
    parser.add_argument('-x', '--nx', action='store', type=int, help="Minimum transcript expression value, denoted Normalized eXpression (NX)", required=False, default=1)
    args = parser.parse_args()

    normal_tissue = args.normal_tissue
    vcf = args.vcf
    nx = args.nx

    thpa_dictionary = build_thpa_dictionary(normal_tissue, min_nx = nx)
    find_expressed_variants(vcf, thpa_dictionary)

    
if  __name__ == "__main__":
    main()

