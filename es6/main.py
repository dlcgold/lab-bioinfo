import sys
from Bio import SeqIO

out = open('output.fq', 'w')
q = int(sys.argv[1])
s = float(sys.argv[2])
if s < 0 or s > 1:
    print("percentuale insensata, uscita")
    exit()
record_fastaq = list(SeqIO.parse("./input.fq", "fastq"))
for feat in record_fastaq:
    if sum([1 if elem > q else 0
            for elem in feat._per_letter_annotations["phred_quality"]]) / len(
            feat._per_letter_annotations["phred_quality"]) > s:
        out.write('@' + feat.id + '\n')
        out.write(str(feat.seq[0:[feat._per_letter_annotations["phred_quality"].index(
            i) for i in feat._per_letter_annotations["phred_quality"] if i < q][0]]) + '\n')
        out.write('+' + feat.name + '\n')
        out.write(
            "".join([chr(elem + 33) for elem in feat._per_letter_annotations["phred_quality"][0:[feat._per_letter_annotations["phred_quality"].index(i) for i in feat._per_letter_annotations["phred_quality"] if i < q][0]]]) + '\n')
