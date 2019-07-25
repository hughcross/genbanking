#!/usr/bin/env python


import sys
import argparse
from gb_parsers.genbank_parsers import parse_genbank_features, parse_gb_feature_dict

# for user inputs
parser = argparse.ArgumentParser(description='create table from genbank information')

parser.add_argument('-i', '--input_filelist', dest='input',
type=str,
help='file with list of gb files (one per line)')

parser.add_argument('-o', '--table_file', dest='out',
type=str,
help='output tab-delimited file')

args = parser.parse_args()
gb_filelist = args.input
tab_file = args.out

### parse the genbank files, add info to dictionary
tableDict = {}

filelist = open(gb_filelist, 'r')
for line in filelist:
    line = line.strip('\n')
    # annotate each file
    annotations = parse_genbank_features(line)
    annots = annotations[0]
    feats = annotations[1]
    features = parse_gb_feature_dict(feats)
    source_feats = features[0]
    for k,v in annots.items():
        tableDict.setdefault(k, {})['accession']=v['seq_name']
        tableDict.setdefault(k, {})['description']=v['description']
    for key,value in source_feats.items():
        if 'country' in value:
            tableDict.setdefault(key, {})['country']=value['country'][0]
        if 'isolate' in value:
            tableDict.setdefault(key, {})['isolate']=value['isolate'][0]
        tableDict.setdefault(key, {})['organism']=value['organism'][0]


## output to file
output = open(tab_file, 'w')

## order of table:
tableOrder = ['organism','accession','country','isolate','description']

for item in tableOrder:
    output.write(item+'\t')
output.write('\n')

for k,v in tableDict.items():
    for para in tableOrder:
        if para in v:
            output.write(v[para]+'\t')
        else:
            output.write('\t')
    output.write('\n')

output.close()






