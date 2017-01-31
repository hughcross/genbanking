#!/usr/bin/env python

# ## Parsing genbank files to extract sequences and output to fasta file

import sys
import argparse

from gb_parsers.genbank_parsers import *

# for user inputs
parser = argparse.ArgumentParser(description='extract sequences from genbank files into fasta')

parser.add_argument('-i', '--input_genbank', dest='input',
type=str,
help='Genbank file from which features will be extracted')

parser.add_argument('-o', '--fasta_file', dest='fa',
type=str,
help='output fasta file (include path if necessary)')
## add arguments for different naming options
#parser.add_argument('--feature', dest='feature', action='store_true')
parser.add_argument('-a', '--accession', action="store_true", dest='accession', default=False,
    help='Use Accession code instead of GI')
parser.add_argument('-g', '--gi_to_num', action="store_true", dest='gi_num', default=False,
    help='add gi in front of number')
parser.add_argument('-d', '--description', action="store_true", dest='description', default=False,
    help='add description after sequence name')
parser.add_argument('-G', '--gene', action="store_true", dest='gene_name', default=False,
    help='add gene name after sequence name')
parser.add_argument('-n', '--note', action="store_true", dest='gene_note', default=False,
    help='add any gene notes after gene name')
## argparse arguments
args = parser.parse_args()
gb_file = args.input
seq_file = args.fa

# files to read and write (required)
seq_dict = genbank_to_seqdict(gb_file)
output = open(seq_file, 'w')

# if options activated, then need to further parse (later 'if' statement to save compute time for simple jobs)
annotations = parse_genbank_features(gb_file)
annots = annotations[0]
feats = annotations[1]
features = parse_gb_feature_dict(feats)
gene_info = features[2]

for k,v in seq_dict.iteritems():
    if args.accession: 
        name = annots[k]['seq_name']
        epithet = k.split(':')[0] 
        newname = epithet+':'+name
    elif args.gi_num: #g == 'yes':
        newname = k.replace(':',':gi')
    else:
        newname = k
    seqline = newname
    if args.gene_name: 
        gene = gene_info[k]['gene']
        genestr = ''
        for gen in gene:
            genestr = genestr+' '+gen
        seqline = seqline +genestr # doing it like this allows adding both gene and description
    if args.gene_note: 
        if 'note' in gene_info[k]:
            notestr = ''
            notes = gene_info[k]['note']
            for nt in notes:
                notestr = notestr + ' '+nt
            seqline = seqline +notestr # doing it like this allows adding both gene and description
    if args.description: 
        descript = annots[k]['description']
        seqline = seqline + ' '+descript
    output.write('>'+seqline+'\n'+v+'\n')
output.close()
