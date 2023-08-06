#!/usr/bin/env python

__author__ = "Alessandro Coppe"
'''
Given a file (-f) with a list of single nucleotide variant positions (chromosome position) and a bam (-b), 
it returns the nucleotide frequences in each position
'''

import pysam
import argparse
import sys

def get_alignment_info_in_position(alignmentfile, chromosome, pos):
    nucleotides_in_pos = {"A":0, "C":0, "G":0, "T":0}
    for pileupcolumn in alignmentfile.pileup(chromosome, pos, pos + 1):
        if pileupcolumn.pos == pos:
           for pileupread in pileupcolumn.pileups:
               if not pileupread.is_del and not pileupread.is_refskip:
                   nucleotide = pileupread.alignment.query_sequence[pileupread.query_position]
                   nucleotides_in_pos[nucleotide] += 1
    return nucleotides_in_pos

def get_positions_from_file(positions_file):
    positions_from_file = []
    i = 1
    for line in positions_file:
        line = line[:-1]
        splitted_line = line.split(" ")
        if len(splitted_line) < 2:
            return -2,i
        try:
            int(splitted_line[1])
        except:
            return -1,i

        positions_from_file.append(splitted_line)
        i += 1
    positions_file.close()
    return positions_from_file,i

def main():
    parser = argparse.ArgumentParser(description="Get VAF info from a .bam file")
    parser.add_argument('-f', '--file', action='store', type=argparse.FileType('r'), help="The path to the positions file (Two tab separated columns file with chromosome\tposition)", required = True, default = None)
    parser.add_argument('-b', '--bam', action='store', type=str, help="The path to the bam file", required = True, default = None)
    args = parser.parse_args()

    positions_file = args.file
    bam = args.bam

    try:
        f = open(bam, 'r')
        f.close()
    except:
        sys.exit("No such bam file: {}".format(bam))

    positions_from_file,i = get_positions_from_file(positions_file)

    if positions_from_file == -1:
        sys.exit("The position is not an int")
    if positions_from_file == -2:
        sys.exit("There are less than 2 columsn in line {}".format(i))

    mybam = pysam.AlignmentFile(bam, "rb")

    print("Position\tA\tC\tG\tT\tCoverage")
    for position in positions_from_file:
        alignment_info_in_position = get_alignment_info_in_position(mybam, position[0], int(position[1]) - 1)
        print("{}:{}\t{}\t{}\t{}\t{}\t{}".format(position[0],position[1],
            alignment_info_in_position['A'], 
            alignment_info_in_position['C'],
            alignment_info_in_position['G'],
            alignment_info_in_position['T'],
            sum(list(alignment_info_in_position.values())))
            )

if  __name__ == "__main__":
    main()

