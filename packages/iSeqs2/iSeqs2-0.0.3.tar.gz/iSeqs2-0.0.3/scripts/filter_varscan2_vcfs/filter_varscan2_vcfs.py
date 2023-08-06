#!/usr/bin/env python

__author__ = "Alessandro Coppe"

'''
Given a set of directories with VarScan2 VCFs obtained from iWhale or vs_format_converter.py (varscan_accessories)
it filters it using somaticFilter command from varscan.jar software
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


def main():
    parser = argparse.ArgumentParser(description="Filter out VCFS produced by VarScan2")
    parser.add_argument('-c', '--min_coverage', action='store', type=int, help="Minimum read depth [20]", required=False, default=20)
    parser.add_argument('-r', '--min_reads2', action='store', type=int, help="Minimum supporting reads for a variant [5]", required=False, default=5)
    parser.add_argument('-s', '--min_strands2', action='store', type=int, help="Minimum # of strands on which variant observed (1 or 2) [1]", required=False, default=1)
    parser.add_argument('-q', '--min_avg_qual', action='store', type=int, help="Minimum average base quality for variant-supporting reads [30]", required=False, default=30)
    parser.add_argument('-f', '--min_var_freq', action='store', type=float, help="Minimum variant allele frequency threshold [0.05]", required=False, default=0.05)
    parser.add_argument('-p', '--p_value', action='store', type=float, help="Default p-value threshold for calling variants [0.05]", required=False, default=0.05)
    parser.add_argument('-d', '--directory', action='store', type=str, help="The directory containing VarScan2 VCFs", required=False, default='.')
    parser.add_argument('-o', '--output_directory', action='store', type=str, help="The output directory", required=False, default='.')
    args = parser.parse_args()

    min_coverage     = args.min_coverage
    min_reads2       = args.min_reads2
    min_strands2     = args.min_strands2
    min_avg_qual     = args.min_avg_qual
    min_var_freq     = args.min_var_freq
    p_value          = args.p_value
    directory        = args.directory
    output_directory = args.output_directory

    if os.path.isdir(directory) == False:
        print(bcolors.ERROR + "{} is not a directory".format(directory) + bcolors.ENDC )
        sys.exit()

    if os.path.isdir(output_directory) == False:
        print(bcolors.ERROR + "{} is not a directory".format(output_directory) + bcolors.ENDC )
        sys.exit()

    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if os.path.isfile(path):
            spliced_input_name = entry.split("_")
            spliced_input_name = spliced_input_name[:len(spliced_input_name) - 1]
            spliced_input_name = "_".join(spliced_input_name)
            output_name = spliced_input_name + "_varscan_filtered.vcf"
            output_file_path = os.path.join(output_directory, output_name)

            command = ["java", "-jar", "/home/ale/local/varscan.jar", "somaticFilter", path, "--output-file", output_file_path, "--min-coverage", str(min_coverage), "--min-reads2", str(min_reads2), "--min-strands2", str(min_strands2), "--min-avg-qual", str(min_avg_qual), "--min-var-freq", str(min_var_freq), "--p-value", str(p_value)]
            print(bcolors.OKGREEN + " ".join(command) + bcolors.ENDC)
            subprocess.run(command)

if __name__ == "__main__":
    main()
