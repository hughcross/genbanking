#!/usr/bin/env python
# coding: utf-8

# ## Parsing genbank files to extract cds info and output to sqlite DB
import sys
import argparse
import sqlite3
#from genbank_parsers import *
from gb_parsers.genbank_parsers import *

# for user inputs
parser = argparse.ArgumentParser(description='To add seq features from genbank files into sqlite DB')

parser.add_argument('-i', '--input_genbank', dest='input',
type=str,
help='Genbank file from which features will be extracted')

parser.add_argument('-db', '--database_file', dest='db',
type=str,
help='sqlite database name (include path if necessary)')

## argparse arguments
args = parser.parse_args()
gb_file = args.input
sqlite_file = args.db

# obtain dictionaries from modules
parsed_file = parse_genbank_features(gb_file)
annots = parsed_file[0]
feats = parsed_file[1]
reclist = feats.keys()
features = parse_gb_feature_dict(feats)
src_dict = features[0]
cds_dict = features[1]

# ### Write dictionaries to sql database
table1 = 'Sequence_Annotations'
table2 = 'CDS_Ranges'
rec = 'Record'
field_type = 'TEXT'
num_type = 'INTEGER'

# connecting to db file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# list to sort table column order
column_ord1 = ['Description', 'Keywords', 'Rec_Name', 'GI', 'Protein_ID', 'Pubmed']
labels = {'Description': 'description', 'Keywords': 'keywords', 'Rec_Name': 'seq_name', 'GI':'gi', 'Pubmed': 'pubmed_id'}

# first add all record ids as keys, then will update with all subsequent columns
for record in reclist:
    sp = [(record)]
    c.execute('INSERT OR IGNORE INTO {tn} ({idf}) VALUES (?)'.format(tn=table1, idf=rec), sp)

conn.commit()

# now more at once >> WORKING FOR NOW
for k,v in annots.iteritems():
    sp = k
    for col in column_ord1:
        if col == 'Protein_ID':
            #continue
            if k in cds_dict:
                value = cds_dict[k]['ncbi_protein_id'][0]
            else:
                value = 'none'
        else:
            lab = labels[col]
            if lab == 'keywords':
                value = v[lab][0]
            else:
                value = v[lab]
        c.execute('''UPDATE Sequence_Annotations SET "{nc}"=? WHERE Record=?'''.format(nc=col), (value, sp))


conn.commit()
# Now add in columns, but need to differentiate between int and text
# try to do in two rounds, one for src dict, and other for cds
# overall order: mol-type, seq-start
col_ord_src = ['Molecule_Type', 'Seq_Start', 'Seq_End']
col_ord_cds = ['Product', 'CDS_Start', 'CDS_End', 'CDS_Orientn', 'Translation']
src_labels = {'Molecule_Type': 'molecule_type', 'Seq_Start': 'start', 'Seq_End': 'end'}
cds_labels = {'Product': 'cds_product', 'CDS_Start': 'cds_start', 'CDS_End': 'cds_end', 'CDS_Orientn': 'cds_orient', 'Translation': 'cds_translation'}


# differentiate between text and num
text = ['Molecule_Type', 'Product', 'CDS_Orientn', 'Translation']
nums = ['Seq_Start', 'Seq_End', 'CDS_Start', 'CDS_End']

# first insert keys
for record in reclist:
    sp = [(record)]
    c.execute('INSERT OR IGNORE INTO {tn} ({idf}) VALUES (?)'.format(tn=table2, idf=rec), sp)

conn.commit()

# now add src data to table:
for k,v in src_dict.iteritems():
    sp = k
    for col in col_ord_src:
        if col == 'Protein_ID':
            #continue
            value = cds_dict[k]['ncbi_protein_id'][0]
        else:
            lab = src_labels[col]
            if lab == 'molecule_type':
                value = v[lab][0]
            else:
                value = v[lab]
        c.execute('''UPDATE CDS_Ranges SET "{nc}"=? WHERE Record=?'''.format(nc=col), (value, sp))

conn.commit()

# repeat with cds data
for k,v in cds_dict.iteritems():
    sp = k
    for col in col_ord_cds:
        if col == 'Protein_ID':
            #continue
            value = cds_dict[k]['ncbi_protein_id'][0]
        else:
            lab = cds_labels[col]
            if lab == 'cds_product':
                value = v[lab][0]
            elif lab == 'cds_translation':
                value = v[lab][0]
            else:
                value = v[lab]
        #print value
        c.execute('''UPDATE CDS_Ranges SET "{nc}"=? WHERE Record=?'''.format(nc=col), (value, sp))

conn.commit()
