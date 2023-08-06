#!/usr/bin/env python


"""

A script that filters a VCF produced by Strelka2 by these parameters:
    - SDP: number of reads with deletions spanning this site at tier1
    - DP: read depth for tier1 (used+filtered)
    - QSS_NT: Quality score reflecting the joint probability of a somatic variant and NT
    - FDP: Number of basecalls filtered from original read depth for tier1

Read https://sites.google.com/site/strelkasomaticvariantcaller/home/somatic-variant-output for more information on
filtering Strelka2

"""

import argparse
import os.path
import sys

def main():
    parser = argparse.ArgumentParser(description="Filter Strelka2 VCF by SDP / DP, QSS_NT and FDP")
    parser.add_argument('-r', '--ratio', action='store', type=float, help="The ration between SDP and DP should be smaller than -r varlue (default = 0.75)", required=False, default=0.75)
    parser.add_argument('-q', '--qss_nt', action='store', type=float, help="Quality score reflecting the joint probability of a somatic variant and NT", required=False, default=15)
    parser.add_argument('-f', '--fdp', action='store', type=float, help="Number of basecalls filtered from original read depth for tier1", required=False, default=4)
    parser.add_argument('-v', '--vcf', action='store', type=str, help="The vcf to be filtered")
    args = parser.parse_args()
    args = parser.parse_args()

    vcf = args.vcf
    ratio_threshold = args.ratio
    qss_nt_threshold = args.qss_nt
    fdp_threshold = args.fdp

    vcf_exists = os.path.isfile(vcf)
    if vcf_exists == False:
        print("File {} do not exists".format(vcf))
        sys.exit(1)

    is_a_strelka_vcf = False


    # Check if args.vcf is a strelka VCF file
    with open(vcf) as vcf_content:
        for line in vcf_content.readlines():
            if line.startswith("#"):
                if line.startswith("##content=strelka"):
                    is_a_strelka_vcf = True
                    break

        if is_a_strelka_vcf == False:
            sys.exit("Not a strelka VCF")

    vcf_content.close()


    ################### Do the job ##################

    pass_ratio_threshold = False
    pass_qss_nt_threshold = False
    pass_fdp_threshold = False

    with open(vcf) as vcf_content:
        for line in vcf_content.readlines():
            if line.startswith("#"):
                print(line[:-1])
            else:
                splitted_line = line.split()
                splitted_format = splitted_line[10].split(":")
                dp = splitted_format[3]
                sdp = splitted_format[6]
                fdp = int(splitted_format[4])
                ratio = float(sdp) / float(dp)
                if ratio < ratio_threshold:
                    pass_ratio_threshold = True

                info = splitted_line[7]
                splitted_info = info.split(";")
                for single_info in splitted_info:
                    if single_info.startswith("QSS_NT="):
                        qss_nt = single_info[7:]
                        qss_nt = int(qss_nt)
                        if qss_nt > qss_nt_threshold:
                            pass_qss_nt_threshold = True


                if fdp <= pass_fdp_threshold:
                    pass_fdp_threshold = True

                if pass_ratio_threshold and pass_qss_nt_threshold and pass_fdp_threshold:
                    #print(pass_ratio_threshold, pass_qss_nt_threshold, pass_fdp_threshold)
                    print(line[:-1])

 

if  __name__ == "__main__":
    main()
