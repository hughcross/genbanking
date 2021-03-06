

# function for parsing blast file
def blast_parser(blastfile, tab='standard'):
    """parse tabular blast files to retrieve all information for downstream"""
    blast = open(blastfile)
    if tab is 'standard': #'standard': # alternative add later
        fmt_list = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
    else:
        fmt_list = tab
    integers = ['qlen','slen','qstart','qend','sstart','send','length','nident','mismatch','positive','gapopen','gaps','qcovs','qcovhsp']
    floaters = ['bitscore','score','pident','ppos','evalue']
    ranges = {}
    rng_index = {}
    hit_index = {}
    hit_dict = {}
    hitlist = []
    # adding list of queries to pass to tuple, to preserve order of queries
    query_list = []
    hit_order = []
    fld_range = len(fmt_list)
    ct = 0
    for hit in blast:
        hit = hit.strip('\n')
        parts = hit.split('\t')
        for fld in range(0,fld_range):
            fld_name = fmt_list[fld]
            # differentiate between field types
            if fld_name in integers:
                fld_value = int(parts[fld])
            elif fld_name in floaters:
                fld_value = float(parts[fld])
            else:
                fld_value = parts[fld]
            if fld == 0:
                if fld_value in hitlist:
                    ct += 1
                else:
                    hitlist.append(fld_value)
                    ct = 0
                hitnum = str(fld_value)+';hit'+str(ct)
                rng_index.setdefault(str(fld_value), []).append(hitnum)
                if fld_value not in query_list:
                    query_list.append(fld_value)

            ranges.setdefault(hitnum, {})[fld_name]=fld_value
            if hitnum not in hit_order:
                hit_order.append(hitnum)
    return(rng_index, ranges, query_list, hit_order)

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

def filter_blast(blast_result_dict, blast_parameters):
    """Filter a blast result dictionary based on variable parameters"""
    ## >> have to add more to following
    field_match = {'SUB_LENGTH':'slen','MIN_QSTART':'qstart','MAX_QSTART':'qstart','MIN_QEND':'qend','MAX_QEND':'qend','MIN_SEND':'send','MAX_SEND':'send','MIN_BITSCORE':'bitscore','MIN_POSITIVE':'positive','MAX_GAPOPEN':'gapopen','MAX_GAPS':'gaps','IN_TITLE':'stitle','IN_SSEQ':'sseq','MIN_SSTART':'sstart','MAX_SSTART':'sstart','MIN_QCOV':'qcovs','MIN_LENGTH':'length','MIN_PCT_ID':'pident','MAX_MISMATCH':'mismatch','MAX_EVALUE':'evalue','IN_SUBJECT_ID':'sseqid'}
    mins = ['MIN_LENGTH','MIN_PCT_ID','MIN_SSTART','MIN_QCOV','SUB_LENGTH','MIN_QSTART','MIN_QEND','MIN_SEND','MIN_BITSCORE','MIN_POSITIVE'] 
    maxes = ['MAX_MISMATCH','MAX_EVALUE','MAX_SSTART','MAX_QSTART','MAX_QEND','MAX_SEND','MAX_GAPOPEN','MAX_GAPS'] 
    containers = ['IN_SUBJECT_ID','IN_TITLE','IN_SSEQ']
    filtered_blast = {}
    blast_parameters.pop('FORMAT')
    num_conditions = len(blast_parameters)
    query_index = blast_result_dict[0]
    hit_results = blast_result_dict[1]
    #>> have to add option for limiting results to the single best match
    for key, value in query_index.iteritems():
        # add dictionary of lists for each hit, and then sort after all hits processed
        for hit in value: # now loops through lists of hits for this query
            conditions_reached = 0
            hit_dict = hit_results[hit]
            # now test all conditions separately
            for k,v in blast_parameters.iteritems():
                blast_field = field_match[k]
                if k in mins:
                    if hit_dict[blast_field] > v:
                        conditions_reached += 1
                elif k in maxes:
                    if hit_dict[blast_field] < v:
                        conditions_reached += 1
                elif k in containers:
                    if v in hit_dict[blast_field]: # need to fix this, was in v
                        conditions_reached += 1

            if conditions_reached == num_conditions:
                filtered_blast[hit]=hit_dict
    return filtered_blast
