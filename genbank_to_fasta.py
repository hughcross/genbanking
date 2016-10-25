#!/usr/bin/env python

# ## Parsing genbank files to extract sequences and output to fasta file

import sys
import argparse

from gb_parsers.genbank_parsers import genbank_to_seqdict

# for user inputs
parser = argparse.ArgumentParser(description='extract sequences from genbank files into fasta')

parser.add_argument('-i', '--input_genbank', dest='input',
type=str,
help='Genbank file from which features will be extracted')

parser.add_argument('-o', '--fasta_file', dest='fa',
type=str,
help='output fasta file (include path if necessary)')

## argparse arguments
args = parser.parse_args()
gb_file = args.input
seq_file = args.fa

seq_dict = genbank_to_seqdict(gb_file)

output = open(seq_file, 'w')
for k,v in seq_dict.iteritems():
    output.write('>'+k+'\n'+v+'\n')
output.close()