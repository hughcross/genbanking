

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

            ranges.setdefault(hitnum, {})[fld_name]=fld_value
    return(rng_index, ranges)

def get_parameters(parameter_file):
    para_file = open(parameter_file, 'r')
    para_dict = {}
    for line in para_file:
        line = line.strip('\n')
        if line.startswith('#'):
            continue
        else:
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
    return para_dict
