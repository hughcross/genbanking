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
parser.add_argument('-I', '--min_pct_id', dest='minpID',
type=int,
help='minimum percent of identical matches (pident) [optional]')
parser.add_argument('-Q', '--min_query_cov', dest='qcoverage',
type=int,
help='minimum query coverage (qcov) [optional]')
parser.add_argument('-B', '--min_bitscore', dest='minbit',
type=int,
help='minimum Bit score (bitscore) [optional]')
parser.add_argument('-G', '--max_gapopen', dest='gapops',
type=int,
help='maximum number of gap openings (gapopen) [optional]')
parser.add_argument('-E', '--min_evalue', dest='ev',
type=int,
help='minimum Evalue (evalue) [optional]')
## >>> add more arguments for other options
## argparse arguments
args = parser.parse_args()
blastfile = args.input
blastout = args.out
parameter_file = args.para
min_length = args.minl
min_pct_id = args.minpID
qcov = args.qcoverage
bit = args.minbit
gap = args.gapops
evalue = args.ev
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
if args.minpID:
    blast_parameters['MIN_PCT_ID']=min_pct_id
if args.qcoverage:
    blast_parameters['QCOV']=qcov
if args.minbit:
    blast_parameters['MIN_BITSCORE']=bit
if args.gapops:
    blast_parameters['MAX_GAPOPEN']=gap
if args.ev:
    blast_parameters['MAX_EVALUE']=evalue
# get blast results
blast_results = blast_parser(blastfile, blast_tab_format)
hit_order = blast_results[3]
# filter blast results
filt_blast_results = filter_blast(blast_results, blast_parameters)

# >> add filter for limiting results to only best hit of group

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
