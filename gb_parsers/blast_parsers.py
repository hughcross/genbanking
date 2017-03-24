
import pandas as pd
import numpy as np 


# function for parsing blast file, note: this is a new one that adds pandas and should speed it up
def blast_parser(blastfile, tab='standard'):
    """parse tabular blast files with pandas to retrieve all information for downstream"""
    blast = open(blastfile)
    if tab is 'standard': #'standard': # alternative add later
        fmt_list = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
    else:
        fmt_list = tab
    # have to assign data types to each field, so they are imported properly
    integers = ['qlen','slen','qstart','qend','sstart','send','length','nident','mismatch','positive','gapopen','gaps','qcovs','qcovhsp']
    floaters = ['bitscore','score','pident','ppos','evalue']
    col_dtypes = {}
    # loop through all fields
    for fld in fmt_list:
        if fld in integers:
            col_dtypes[fld]='int'
        elif fld in floaters:
            col_dtypes[fld]='float'
        else:
            col_dtypes[fld]='str'

    blastDF = pd.read_table(blastfile, sep='\t', dtype=col_dtypes, names=fmt_list)
    
    return blastDF

def get_parameters(parameter_file):
    para_file = open(parameter_file, 'r')
    para_dict = {}
    # identify category of parameter
    integers = ['MIN_LENGTH', 'MIN_NUM_ID', 'MAX_MISMATCH','MIN_QCOV','SUB_LENGTH','MIN_QSTART','MAX_QSTART','MIN_QEND','MAX_QEND','MIN_SSTART','MAX_SSTART','MIN_SEND','MAX_SEND','MIN_POSITIVE','MAX_GAPOPEN','MAX_GAPS']
    floaters = ['MIN_PCT_ID','MAX_EVALUE','MIN_BITSCORE']
    strings = ['IN_SUBJECT_ID','IN_TITLE','IN_SSEQ']
    for line in para_file:
        line = line.strip('\n')
        if line.startswith('#'):
            continue
        else: # >> rewrite to take multiple types
            line_parts = line.split('=')
            para_name = line_parts[0]
            para_value =line_parts[1]
            if para_name == 'FORMAT':
                fieldlist = para_value.split(' ')
                para_dict['FORMAT']=fieldlist
            elif para_name in integers:
                para_dict[para_name]=int(para_value)
            elif para_name in floaters:
                para_dict[para_name]=float(para_value)
            elif para_name in strings:
                para_dict[para_name]=para_value
    return para_dict

def filter_blast(blastDF, blast_parameters):
    """Filter a blast result dictionary based on variable parameters using pandas"""
    ## >> have to add more to following
    field_match = {'SUB_LENGTH':'slen','MIN_QSTART':'qstart','MAX_QSTART':'qstart','MIN_QEND':'qend','MAX_QEND':'qend','MIN_SEND':'send','MAX_SEND':'send','MIN_BITSCORE':'bitscore','MIN_POSITIVE':'positive','MAX_GAPOPEN':'gapopen','MAX_GAPS':'gaps','IN_TITLE':'stitle','IN_SSEQ':'sseq','MIN_SSTART':'sstart','MAX_SSTART':'sstart','MIN_QCOV':'qcovs','MIN_LENGTH':'length','MIN_PCT_ID':'pident','MAX_MISMATCH':'mismatch','MAX_EVALUE':'evalue','IN_SUBJECT_ID':'sseqid'}
    mins = ['MIN_LENGTH','MIN_PCT_ID','MIN_SSTART','MIN_QCOV','SUB_LENGTH','MIN_QSTART','MIN_QEND','MIN_SEND','MIN_BITSCORE','MIN_POSITIVE'] 
    maxes = ['MAX_MISMATCH','MAX_EVALUE','MAX_SSTART','MAX_QSTART','MAX_QEND','MAX_SEND','MAX_GAPOPEN','MAX_GAPS'] 
    containers = ['IN_SUBJECT_ID','IN_TITLE','IN_SSEQ']
    filtered_blast = {}
    blast_parameters.pop('FORMAT')
    num_conditions = len(blast_parameters)
    # for now have to build it as a string and then run 
    string_list = []
    for k,v in blast_parameters.iteritems():
        
        blast_field = field_match[k]
        string = "blastDF[blast_field]"
        if k in mins:
            
            string = string + "> %s" %(v)
            
        elif k in maxes:
            string = string + "< %s" %(v)
            
                
        elif k in containers:
            string = string+".str.contains('%s')" % (v)
            
        string_list.append(string)
    if num_conditions == 1:
        cmd_string = string_list[0]
        final_string = "filt_blastDF = blastDF["+cmd_string+"]"
        exec(final_string)
        
    # for multiple conditions:
    #blast3 = blast_table[(blast_table['pident'] > 35) & (blast_table['length'] > 100)]
    else:
        initial = "filt_blastDF = blastDF["
        for cmd in string_list:
            new_string = "("+cmd+")"
            initial = initial+new_string+"&"
        semifinal = initial[:-1]
        final = semifinal+"]"
        exec(final)
    return filt_blastDF
    