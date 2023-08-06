#!/usr/bin/env python

__author__ = "Alessandro Coppe"

'''
Given tables created by............................
'''

import argparse
import os.path
import os
import sys
import pathlib
import subprocess


class bcolors:
    OKGREEN = '\033[92m'
    ERROR   = '\033[91m'
    ENDC    = '\033[0m'



def get_info_from_patient_mutation(format, patient_data, caller):
    returned_dict = {}
    if "\n" in patient_data:
        patient_data = patient_data[:-1]
    patient_data = patient_data.split(":")
    # GT: genotype
    gt = patient_data[0]
    returned_dict["gt"] = gt

    if caller == "mutect2" or caller == "mutect":
        # Allelic depths for the ref and alt alleles in the order listed
        AD_alleles_depth = patient_data[1]
        normal = AD_alleles_depth.split(",")[0]
        tumor = AD_alleles_depth.split(",")[1]
        vaf = float(tumor) / ( float(tumor) + float(normal))
        coverage = int(tumor) + int(normal)
        returned_dict["vaf"] = vaf
        returned_dict["coverage"] = coverage
        returned_dict["normal"] = normal
        returned_dict["tumor"] = tumor


    if caller == "haplotypecaller":
        # Allelic depths for the ref and alt alleles in the order listed
        AD_alleles_depth = patient_data[1]
        normal = AD_alleles_depth.split(",")[0]
        tumor = AD_alleles_depth.split(",")[1]
        addition = (float(tumor) + float(normal))
        if addition == 0:
            return None
        vaf = float(tumor) / ( float(tumor) + float(normal))
        coverage = int(tumor) + int(normal)
        returned_dict["vaf"] = vaf
        returned_dict["coverage"] = coverage
        returned_dict["normal"] = normal
        returned_dict["tumor"] = tumor

    if caller == "varscan":
        # DP: Read Depth (coverage) Total depth of quality bases
        coverage = patient_data[2]
        # RD: Depth of reference-supporting base
        normal = patient_data[3]
        # AD: Depth of variant-supporting bases (reads2) tumor bases
        tumor = patient_data[4]
        # FREQ: Variant allele frequency
        vaf = float(tumor) / ( float(tumor) + float(normal))
        returned_dict["coverage"] = coverage
        returned_dict["normal"] = normal
        returned_dict["tumor"] = tumor
        returned_dict["vaf"] = vaf

    if caller == "strelka":
        splitted_format = format.split(":")
        if splitted_format[1] == "BCN50":
            tar = patient_data[7]
            tir = patient_data[8]
            normal = int(tar.split(",")[0])
            tumor = int(tir.split(",")[0])
            coverage = normal + tumor
            vaf = float(tumor) / (float(normal) + float(tumor))
            returned_dict["normal"] = normal
            returned_dict["tumor"] = tumor
            returned_dict["vaf"] = vaf
            returned_dict["coverage"] = coverage
        else:
            nucleotides_freq = {"a": patient_data[1],
                "c": patient_data[2],
                "g": patient_data[5],
                "t": patient_data[8]}
            keys = nucleotides_freq.keys()
            values = nucleotides_freq.values()
            new_values = [int(el.split(",")[0]) for el in values]
            new_nucleotides_freq = dict(zip(keys, new_values))
            new_values.sort()
            # DP: Read Depth
            coverage = sum(new_values)
            # RD: Depth of reference-supporting base
            rd = sum(new_values) - sum(new_values[:-1])
            # AD: Depth of variant-supporting bases (reads2)
            ad = new_values[-2]
            normal_nucleotide_freq = new_values[-1]
            tumor_nucleotide_freq = new_values[-2]
            frequency = float(tumor_nucleotide_freq) / (tumor_nucleotide_freq + normal_nucleotide_freq)
            returned_dict["normal"] = normal_nucleotide_freq
            returned_dict["tumor"] = tumor_nucleotide_freq
            returned_dict["vaf"] = frequency
            returned_dict["coverage"] = int(tumor_nucleotide_freq) + int(normal_nucleotide_freq)

    return returned_dict


def build_output_line(line, caller):
    # It returns:
    # CHROM POITION IDS ALTERNATIVE NORMAL PASS CLNSIG 1/0 COVERAGE TUMOR NORMAL VAF GENE EFFECT
    splitted_line = line.split("\t")
    first_part_of_output = splitted_line[0:6]
    splitted_effects = splitted_line[7].split(",")
    splitted_genes = splitted_line[6].split(",")
    genes_effects = list(zip(splitted_genes,splitted_effects))
    genes_effects = list(set(genes_effects))
    genes_effects = [g_e for g_e in genes_effects if g_e[1] in ["MODERATE", "HIGH"]]
    clnsig = splitted_line[8]
    first_part_of_output.append(clnsig)
    file_format = splitted_line[9]
    if caller == "haplotypecaller":
        tumor_data = 10
        tumor_data = get_info_from_patient_mutation(file_format, splitted_line[tumor_data], "haplotypecaller")
        if tumor_data == None:
            return None

    if caller == "mutect2":
        gt1 = splitted_line[11].split(":")[0]
        gt2 = splitted_line[10].split(":")[0]
        if gt1 == "0/1" or gt1 == "1/0":
            tumor_data = 11
        else:
            tumor_data = 10
        tumor_data = get_info_from_patient_mutation(file_format, splitted_line[tumor_data], "mutect2")
        #normal_data = get_info_from_patient_mutation(file_format, splitted_line[10], "mutect2")
    if caller == "mutect":
        gt1 = splitted_line[11].split(":")[0]
        gt2 = splitted_line[10].split(":")[0]
        if gt1 == "0/1" or gt1 == "1/0":
            tumor_data = 11
        else:
            tumor_data = 10
        tumor_data = get_info_from_patient_mutation(file_format, splitted_line[tumor_data], "mutect")
    # Check if variants with normal high VAF are rigth
    if caller == "varscan":
        tumor_data = get_info_from_patient_mutation(file_format, splitted_line[11], "varscan")
    if caller == "strelka":
        tumor_data = get_info_from_patient_mutation(file_format, splitted_line[11], "strelka")


    first_part_of_output.append(tumor_data.get("gt"))
    first_part_of_output.append(str(tumor_data.get("coverage")))
    first_part_of_output.append(str(tumor_data.get("tumor")))
    first_part_of_output.append(str(tumor_data.get("normal")))
    first_part_of_output.append(str(tumor_data.get("vaf")))
    effects = []
    for gene_effect in genes_effects:
        effects.append(gene_effect[1])
    gene = gene_effect[0]
    if "HIGH" in effects:
        effect = "HIGH"
    else:
        effect = "MODERATE"

    first_part_of_output.append(gene)
    first_part_of_output.append(effect)
    return first_part_of_output

def clean_sample_names(list_of_available_files):
    sample_names = []
    l = [f for f in list_of_available_files if not f.startswith(".")]
    for name in l:
        i = 0
        splitted_name = name.split("_")
        for el in splitted_name:
            if el in ["mutect", "strelka", "mutect2", "varscan"]:
                sample_name = splitted_name[:(i)]
                sample_names.append("_".join(sample_name))
                break
            if el in ["none"]:
                sample_name = splitted_name[:(i + 1)]
                sample_names.append("_".join(sample_name))
                break
            i += 1
    sample_names = list(set(sample_names))
    return(sample_names)


def main():
    parser = argparse.ArgumentParser(description="Join all the tables produced by SnpSift extractFields")
    parser.add_argument('-d', '--directory', action='store', type=str, help="The directory containing all the files to be joined", required=True)
    args = parser.parse_args()

    directory = args.directory

    if os.path.isdir(directory) == False:
        print(bcolors.ERROR + "{} is not a directory".format(directory) + bcolors.ENDC )
        sys.exit()

    variants = {}

    all_files = os.listdir(directory)
    all_files.sort()
    sample_names = list(set(["_".join(f.split("_")[:4]) for f in all_files]))
    sample_names = clean_sample_names(all_files)
    for sample in sample_names:
        mutations = {}
        mutation_lines = {}
        sample_files = [f for f in all_files if f.startswith(sample)]

        for entry in sample_files:

            if "_mutect2_" in entry:
                f = open(os.path.join(directory, entry))
                for line in f:
                    if not line.startswith("#") and not line.startswith("CHROM"):
                        output_line = "\t".join(build_output_line(line, "mutect2"))
                        the_key = output_line.split("\t")[0] + output_line.split("\t")[1]
                        if the_key not in mutation_lines.keys():
                            mutation_lines[the_key] = []
                            mutation_lines[the_key] = output_line
                        if  the_key not in mutations.keys():
                            mutations[the_key] = []
                            mutations[the_key].append("mutect2")
                        else:
                            mutations[the_key].append("mutect2")

            elif "_mutect_" in entry:
                f = open(os.path.join(directory, entry))
                for line in f:
                    if not line.startswith("#") and not line.startswith("CHROM"):
                        output_line = "\t".join(build_output_line(line, "mutect"))
                        the_key = output_line.split("\t")[0] + output_line.split("\t")[1]
                        if the_key not in mutation_lines.keys():
                            mutation_lines[the_key] = []
                            mutation_lines[the_key] = output_line
                        if  the_key not in mutations.keys():
                            mutations[the_key] = []
                            mutations[the_key].append("mutect")
                        else:
                            mutations[the_key].append("mutect")


            elif "varscan" in entry or "varscan2" in entry:
                f = open(os.path.join(directory, entry))
                for line in f:
                    if not line.startswith("#") and not line.startswith("CHROM"):
                        output_line = "\t".join(build_output_line(line, "varscan"))
                        the_key = output_line.split("\t")[0] + output_line.split("\t")[1]
                        if the_key not in mutation_lines.keys():
                            mutation_lines[the_key] = []
                            mutation_lines[the_key] = output_line
                        if  the_key not in mutations.keys():
                            mutations[the_key] = []
                            mutations[the_key].append("varscan")
                        else:
                            mutations[the_key].append("varscan")


            elif "strelka2" in entry or "strelka" in entry:
                f = open(os.path.join(directory, entry))
                for line in f:
                    if not line.startswith("#") and not line.startswith("CHROM"):
                        output_line = "\t".join(build_output_line(line, "strelka"))
                        the_key = output_line.split("\t")[0] + output_line.split("\t")[1]
                        if the_key not in mutation_lines.keys():
                            mutation_lines[the_key] = []
                            mutation_lines[the_key] = output_line
                        if  the_key not in mutations.keys():
                            mutations[the_key] = []
                            mutations[the_key].append("strelka")
                        else:
                            mutations[the_key].append("strelka")

            elif "_none_" in entry:
                f = open(os.path.join(directory, entry))
                for line in f:
                    if not line.startswith("#") and not line.startswith("CHROM"):
                        if build_output_line(line, "haplotypecaller") != None:
                            output_line = "\t".join(build_output_line(line, "haplotypecaller"))
                            the_key = output_line.split("\t")[0] + output_line.split("\t")[1]
                            if the_key not in mutation_lines.keys():
                                mutation_lines[the_key] = []
                                mutation_lines[the_key] = output_line
                            if  the_key not in mutations.keys():
                                mutations[the_key] = []
                                mutations[the_key].append("haplotypecaller")
                            else:
                                mutations[the_key].append("haplotypecaller")



        for key in mutations:
            first_part_of_output = mutation_lines.get(key)
            variant_callers = set(mutations.get(key))
            variant_callers = "-".join(variant_callers)
            entire_line = first_part_of_output + "\t" + variant_callers + "\t" + sample
            print(entire_line)


if __name__ == "__main__":
    main()
