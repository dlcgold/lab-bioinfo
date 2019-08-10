from Bio import SeqIO


out = open('output.txt', 'w')
record = list(SeqIO.parse("./M10041.txt", "embl"))[0]
identifier = record.name
org = record.annotations['data_file_division']

# dalle featurues CDS prendo inizio e fine della sequenza
# e la sequenza della proteina
for i in record.features:
    if i.type == "CDS":
        cds_start = i.location.start
        cds_end = i.location.end
        trans_str = str(i.qualifiers['translation'][0])

# seleziono la parte utile dell'intera sequenza
seq_str = str(record.seq)

# stampo (sequenze in pezzi di 80)
out.write('>'+identifier+'-'+org + '\n')
out.write('\n'.join([seq_str[i:i+80] for i in range(0, len(seq_str), 80)]))
out.write('\n>' + identifier + '-' + org + '; CDS start = ' +
          str(cds_start) + '; CDS end = ' + str(cds_end) + '\n')
out.write('\n'.join([trans_str[i:i+80] for i in range(0, len(trans_str), 80)]))
