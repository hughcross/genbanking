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

`filter_blast_results.py -i example_blast_output_default_format.txt -p parameters_file_template.txt -o example_output`



qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore'


custom:
qseqid sseqid length pident mismatch qcovs evalue bitscore qstart qend sstart send gapopen
