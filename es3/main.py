from Bio import SeqIO
import numpy as np
from collections import Counter

record = list(SeqIO.parse("./M10051.txt", "embl"))[0]
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
seq_str = str(record.seq)[cds_start:cds_end]

gen_file = np.loadtxt('./genetic-code.txt', dtype=str)

# genero il dizionario del file genetic-code
tuple_gen = {}
for elem in gen_file:
    for sub in elem.split(',')[1:]:
        tuple_gen[sub.upper()] = elem[0]

# separo la sequenze in sottosequenze da 60 caratteri
seq_list = [seq_str[i:i+60] for i in range(0, len(seq_str), 60)]

# estraggo la lista dei codoni
cds_codon = [seq_str[i:i+3] for i in range(0, len(seq_str), 3)]

# counter dei codoni
count_codon = Counter(cds_codon)
# trascrizione codoni in amminoacidi (in stringa)
ammino_str = ''.join([tuple_gen[codon]
                      for codon in cds_codon if tuple_gen[codon].isupper()])
ammino_counter = Counter(list(ammino_str))

# output su file come da richiesta
out = open('output.txt', 'w')
out.write('>CDS '+identifier+' '+org + '\n')
out.write('\n'.join(seq_list))
out.write('\n>Distribuzione di frequenza dei codoni\n')
for key, elem in count_codon.most_common():
    out.write(key + ' => ' + str(elem) + '\n')
    out.write('>Distribuzione delle frequenze degli amminoacidi\n')
for key, elem in ammino_counter.most_common():
    out.write(key + ' => ' + str(elem) + '\n')
if ammino_str == trans_str:
    out.write(
        'La traduzione della CDS coincide con la traduzione riportata nel file input')
