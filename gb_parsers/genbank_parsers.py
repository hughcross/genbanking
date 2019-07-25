#!/usr/bin/env python

# note: will try to make this class later
## modules to parse genbank files and extract information for database, conversion to fasta file, etc.
from Bio import SeqIO
from Bio import SeqFeature

def parse_genbank_features(genbank_file):
    """function to parse genbank files to extract features"""
    handle = open(genbank_file, 'r')
    seq_records = SeqIO.parse(handle, 'gb')
    # start by creating one dicts of features 
    feats = {}
    annots = {}
    #seqdict = {} # do this in separate function 
    for rec in seq_records:
        full_epithet = rec.annotations['organism']
        epithet = full_epithet.replace(' ','_').replace('.','')
        name = rec.name
        #if 'gi' in rec.annotations: Taking this option out, as GI being phased out
         #   gi_id = rec.annotations['gi'] 
          #  rec_id = epithet+':'+gi_id
        #else:
        rec_id = epithet+':'+name
        descr = rec.description
        if 'references' in rec.annotations:

            refs = rec.annotations['references']
            ref0 = refs[0]
            if ref0.pubmed_id:
                pub = ref0.pubmed_id
            else:
                pub = 'none'
            annots.setdefault(rec_id, {})['pubmed_id']=pub
        keywords = rec.annotations['keywords']
        # make annot dict
        annots.setdefault(rec_id, {})['keywords']=keywords
        annots.setdefault(rec_id, {})['description']=descr
        annots.setdefault(rec_id, {})['seq_name']=name
        
        #if 'gi' in rec.annotations:

         #   annots.setdefault(rec_id, {})['gi']=gi_id
        #else:
         #   annots.setdefault(rec_id, {})['gi']='none'
        # make sequence dict
        #sequence = str(rec.seq)
        #seqdict[rec_id]=sequence
        # get features to process downstream
        feature = rec.features
        feats[rec_id]=feature
    return (annots, feats)


#reclist = feats.keys()

def parse_gb_feature_dict(feature_dictionary):
    # now try to create dictionaries of ranges, translations, organism, protein id, etc
    src_dict = {}
    cds_dict = {}
    gene_dict = {}
    for k,v in feature_dictionary.items():
        for ft in v:
            if ft.type == 'source':
                src_locs = ft.location
                src_start = int(src_locs.start)
                src_end = int(src_locs.end)
                src_ornt = src_locs.strand
                src_quals = ft.qualifiers
                org = src_quals['organism']
                mol_typ = src_quals['mol_type']
                if 'country' in src_quals:
                    src_dict.setdefault(k, {})['country']=src_quals['country']
                if 'isolate' in src_quals:
                    src_dict.setdefault(k, {})['isolate']=src_quals['isolate']
                src_dict.setdefault(k, {})['start']=src_start
                src_dict.setdefault(k, {})['end']=src_end
                src_dict.setdefault(k, {})['orient']=src_ornt
                src_dict.setdefault(k, {})['organism']=org
                src_dict.setdefault(k, {})['molecule_type']=mol_typ
            elif ft.type == 'CDS':
                cd_locs = ft.location
                cd_start = int(cd_locs.start)
                cd_end = int(cd_locs.end)
                cd_ornt = cd_locs.strand
                cd_quals = ft.qualifiers
                if 'product' in cd_quals:
                    product = cd_quals['product']
                    cds_dict.setdefault(k, {})['cds_product']=product
                if 'translation' in cd_quals:
                    trans = cd_quals['translation']
                    cds_dict.setdefault(k, {})['cds_translation']=trans
                if 'protein_id' in cd_quals:
                    gb_protein = cd_quals['protein_id']
                    cds_dict.setdefault(k, {})['ncbi_protein_id']=gb_protein
                cds_dict.setdefault(k, {})['cds_start']=cd_start
                cds_dict.setdefault(k, {})['cds_end']=cd_end
                cds_dict.setdefault(k, {})['cds_orient']=cd_ornt
            elif ft.type == 'gene':
                #gen = ft.gene
                gen_quals = ft.qualifiers
                gene = gen_quals['gene']
                gene_dict.setdefault(k, {})['gene']=gene
                if 'note' in gen_quals:
                    gene_dict.setdefault(k, {})['note']=gen_quals['note']    
                

    return (src_dict, cds_dict, gene_dict)

def genbank_to_seqdict(genbank_file):
    """function to parse genbank files to extract sequences"""
    handle = open(genbank_file, 'r')
    seq_records = SeqIO.parse(handle, 'gb')
    # start by creating one dicts of features 
    seqdict = {}
    for rec in seq_records:
        full_epithet = rec.annotations['organism']
        epithet = full_epithet.replace(' ','_').replace('.','')
        name = rec.name
        if 'gi' in rec.annotations:
            gi_id = rec.annotations['gi']
            rec_id = epithet+':'+gi_id
        else:
            rec_id = epithet+':'+name
        sequence = str(rec.seq)
        seqdict[rec_id]=sequence
    return seqdict


