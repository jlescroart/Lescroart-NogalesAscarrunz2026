# conda activate fastq2bam
# code generated with ChatGPT on 12JUL23
# Takes a VCF file and discards all transitions, keeping only transversions.

import pysam
import gzip

def is_transversion(ref, alt):
    transitions = {('A', 'G'), ('G', 'A'), ('C', 'T'), ('T', 'C')}
    return (ref, alt) not in transitions and (alt, ref) not in transitions

def filter_vcf(input_vcf, output_vcf):
    with gzip.open(input_vcf, 'rt') as f_in:
        vcf_in = pysam.VariantFile(f_in, 'r')
        vcf_out = pysam.VariantFile(output_vcf, 'w', header=vcf_in.header)

        for record in vcf_in:
            ref = record.ref
            alts = record.alts
            if alts:
                for alt in alts:
                    if is_transversion(ref, alt):
                        vcf_out.write(record)
                        break  # Stop after writing the record once for any valid alt

        vcf_in.close()
        vcf_out.close()

# Provide your input VCF file and the desired output VCF file names
input_vcf = "/media/labgenoma4/DATAPART4/jonasl/data/tigrinus/vcf_Oge1/oncifelis_unmasked.vcf.gz"
output_vcf = "/media/labgenoma4/DATAPART4/jonasl/data/tigrinus/vcf_Oge1/oncifelis_unmasked_Tv.vcf"

filter_vcf(input_vcf, output_vcf)

