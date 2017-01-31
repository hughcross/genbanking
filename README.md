# Genbanking
A collection of scripts to parse and store information from genbank files

This repository is a set of tools to extract information from common NCBI files and outputs. It is based on functions I wrote to cover different options and information available for the NCBI files.
<br></br>
## filter_blast_results.py

*Description:*
After having written many scripts to parse different kinds of blast output, I finally wrote a function that will parse any blast results file that uses tabular format (**-outfmt 6**). The script will assume that you use the default tab format, but it will also read any custom format, as long as you provide the format in a parameters file. 

### Basic Usage

Using a default blast tabular output, you can filter the results to only retain reads with a minimum length of 100:

`filter_blast_results.py -i example_blast_output_default_format.txt -L 100 -o example_output`

You can use multiple filters in the same command, and only those results matching all conditions will be output:

`filter_blast_results.py -i example_blast_output_default_format.txt -L 100 -I 50 -o example_output`

In the above example, results will be filtered for both minimum alignment length (-L) and minimum percent identity (-I). If you do not provide the name of an output file, the program will just add 'filtered_' to the beginning of the output file. 

There are six possible filters that can be entered as command line options. To see all the options, enter:

`filter_blast_results.py -h`
<br></br>
### Adding Additional Parameters

To filter with additional fields, you can make a parameters file to filter with up to 22 blast fields. I have included a template file: *parameters_file_template.txt*, that lists all the options. Make a copy of this file, and just uncomment (take out the # at the start of the line) any field that you want to use, and fill in the appropriate number or text after the = sign. At a minimum you need to indicate the tabular FORMAT used (this file has the default table format set up). The template file is set to search for the same parameters as the second example above, so you can check to see that it is working the same. Add the parameters file using the '-p' option:

`filter_blast_results.py -i example_blast_output_default_format.txt -p parameters_template.txt -o example_output`

I have included the file *descriptions_of_parameters.txt* that describes the different options and what fields they are filtering. 
<br></br>
### Searching for Text in Results

Three parameters can be used to search for text within results. You can search for key words or terms within either the Subject Seq-id (sseqid) or Subject Title (stitle) using the '*IN_SUBJECT_ID*' or '*IN_TITLE*' parameters, respectively. You can also search for DNA or protein sequence motifs within the Subject Sequence (sseq) using the '*IN_SEQ*' parameter. However, the search is simple and will not account for mutations or gaps in the sequence. You can try this on the example blast file: uncomment the '*IN_SUBJECT_ID*' parameter, and rerun the command as above. The example will search for all occurrences of the keyword 'ARATH' in the blast results, which is a Swiss-Prot keyword. You could use this to search for specific gi numbers or taxa, for example. 
<br></br>
### Using Custom Table Formats

As mentioned above, I have set this program up to use custom table formats that are possible through the tabular formatting option. This is one reason I really like this output option when using BLAST. You are able to add any number of options based on what you need for that particular search. I have included an alternative parameter format template: '*custom_format_parameters_template.txt*', which has a custom table format (in the line that starts 'FORMAT='). In this example, I ran a BLAST search using the following command:

`blastn -query input_seqs.fa -db WS77111.fa -max_target_seqs 5 -out example_custom_blast.out -outfmt "6 qseqid sseqid length pident mismatch qcovs evalue bitscore qstart qend sstart send gapopen"`

The only important thing to notice in the above command is how the custom output format is set up. For a complete list of fields, see full BLAST help ('blastn -help'). To filter your own custom blast results, just copy from the format within the quotes (except for the 6), and paste that in a parameters file after 'FORMAT=', and uncomment and amend any other fields you wish to use to filter, and you will be set. Note that even if you call a parameters file, you can override any of the file filters using the command line option, which might be useful if you would like to try different options with a custom tab format.

An example of filtering using custom formatting:

`filter_blast_results.py -i example_custom_blast.out -p custom_format_parameters_template.txt -o example_custom_output`
<br></br>
<br></br>
## genbank_to_fasta.py

Software prerequisite:

* Biopython https://github.com/biopython/biopython.github.io/

*Description:*

This script extracts sequences from genbank format files, renaming the sequences by the taxon, not the gi number, as in the standard Biopython tool. I prefer to have sequence names more descriptive, so this script simply modifies the output from the SeqIO tool, and also allows for additional annotations to be added to the sequence name. 

### Basic Usage

All you need is to name the input file and choose a name for the fasta output. You can test with the supplied example genbank file:

`genbank_to_fasta.py -i genbank_example.gb -o output.fasta`
<br></br>
### Additional Options

The resulting sequence file names will all be in the format genus_species:gi-number, which will look like this:

>\>Senna_occidentalis:169667647 

If you prefer, you can use the accession number with the -a option: 

`genbank_to_fasta.py -i genbank_example.gb -o output.fasta -a`

Which should give you:

>\>Senna_occidentalis:AF365030

You can also add the gene name with -G and gene notes (if the gb file has notes) with -n

`genbank_to_fasta.py -i genbank_example.gb -o output.fasta -G`

>\>Senna_occidentalis:14595386 trnL

The full description can be added after the sequence name with -d. In the following example, the option -g is also used to add a 'gi' to the GI number, to make it more clear:

`genbank_to_fasta.py -i genbank_example.gb -o output.fasta -dg`

>\>Senna_occidentalis:gi14595386 Senna occidentalis voucher Bruneau 1257 (MT) tRNA-Leu (trnL) gene, intron; chloroplast.

You can add both the gene and description to the end of the file, but that will usually be redundant. 


