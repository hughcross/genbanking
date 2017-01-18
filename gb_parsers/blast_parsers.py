

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
            elif para_name == 'MIN_LENGTH':
                para_dict['MIN_LENGTH']=int(para_value)
            elif para_name == 'MIN_PCT_ID':
                para_dict['MIN_PCT_ID']=int(para_value)
            elif para_name == 'QCOV':
                para_dict['QCOV']=int(para_value)
            elif para_name == 'MAX_MISMATCH':
                para_dict['MAX_MISMATCH']=int(para_value)
    return para_dict

def filter_blast(blast_result_dict, blast_parameters):
    """Filter a blast result dictionary based on variable parameters"""
    ## >> have to add more to following
    field_match = {'MIN_LENGTH':'length','MIN_PCT_ID':'pident','MAX_MISMATCH':'mismatch','EVALUE':'evalue','SUBJECT_ID':'sseqid'}
    mins = ['MIN_LENGTH','MIN_PCT_ID'] # have to add to this
    maxes = ['MAX_MISMATCH','EVALUE'] # have to add
    matches = ['SUBJECT_ID']
    filtered_blast = {}
    blast_parameters.pop('FORMAT')
    num_conditions = len(blast_parameters)
    query_index = blast_result_dict[0]
    hit_results = blast_result_dict[1]
    for key, value in query_index.iteritems():
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
                elif k in matches:
                    if hit_dict[blast_field] == v:
                        conditions_reached += 1

            if conditions_reached == num_conditions:
                filtered_blast[hit]=hit_dict
    return filtered_blast
