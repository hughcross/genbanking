#!/usr/bin/env python

# ## parsing and filtering blast files and output to new file

import sys
import argparse

from gb_parsers.blast_parsers import * # >>change this to more direct method

# for user inputs
parser = argparse.ArgumentParser(description='filter blast results')

parser.add_argument('-i', '--input_blast', dest='input',
type=str,
help='BLAST file from which features will be extracted')

parser.add_argument('-o', '--output', dest='out',
type=argparse.FileType('w'),
help='filtered blast file')

parser.add_argument('-p', '--parameters', dest='para',
type=str,
help='parameter file [optional]')
### add argparse arguments for individual filters to avoid using parameter file in simple cases
parser.add_argument('-L', '--min_length', dest='minl',
type=int,
help='minimum alignment length [optional]')
## >>> add more arguments for other options
## argparse arguments
args = parser.parse_args()
blastfile = args.input
blastout = args.out
parameter_file = args.para
min_length = args.minl

# check for parameters file
if args.para:
    blast_parameters = get_parameters(parameter_file)
    # get format
    blast_tab_format = blast_parameters['FORMAT']
else:
    # have to put default format parameters here, in case none provided
    blast_tab_format = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']

## need to catch exception here is no parameters file AND no parameters options on command line
if args.minl:
    blast_parameters['MIN_LENGTH']=min_length
# add more, and exception

# get blast results
blast_results = blast_parser(blastfile, blast_tab_format)
hit_order = blast_results[3]
# filter blast results
filt_blast_results = filter_blast(blast_results, blast_parameters)

# write filtered results to file
for hit in hit_order:
    if hit in filt_blast_results:
        hit_values = filt_blast_results[hit]
        #for key,value in filt_blast_results.iteritems():
        blaststring = ''
        for field in blast_tab_format:
            #print field
            field_value = str(hit_values[field])
            blaststring = blaststring+field_value+'\t'
        blastwrite = blaststring+'\n'
        blastwrite = blastwrite.replace('\t\n','\n')
        blastout.write(blastwrite)
