import re
from Bio import SeqIO


def rev_comp(s):
    # start at string length, end at position 0, move with the step -1
    rc_s = s[::-1]
    rc_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C',
               't': 'a', 'a': 't', 'c': 'g', 'g': 'c', }
    return ''.join([rc_dict[c] for c in rc_s])


out = open('output.fa', 'w')
record_fasta = list(SeqIO.parse("./ENm006.fa", "fasta"))[0]
fasta_seq = str(record_fasta.seq)

with open('./input.gtf', 'r') as gtf_file:
    gtf_rows = gtf_file.readlines()

strand_dict = {}
feat_dict = {}
for row in gtf_rows:
    # splitto sui tab e ottengo in campi
    gtf_list = row.rstrip().split('\t')
    ref_id = gtf_list[0]
    gene_id = re.search('gene_id\s*\"([^"]+)\"', gtf_list[8]).group(1)
    transcript_id = re.search(
        'transcript_id\s*\"([^"]+)\"', gtf_list[8]).group(1)

    if gtf_list[2] in ['exon', 'CDS']:
        # aggiorno il dizionario degli strand
        strand_dict[gene_id] = gtf_list[6]
        key = gtf_list[2]+'$'+gene_id+'$'+transcript_id
        # se ho già la chiave recupero le feature e aggiungo la corrente
        # con gli estremi indicati nei campi 3 e 4
        if key in feat_dict:
            feat_list = feat_dict.pop(key)
            feat_list.append(
                [int(gtf_list[3]), int(gtf_list[4])])
        else:
            # creo lista delle feature
            feat_list = [[int(gtf_list[3]), int(gtf_list[4])]]
            # aggiorno il dizionario
        feat_dict[key] = feat_list
for key in feat_dict:
    if key.split('$')[0] == 'exon':
        # recupero la lista degli esoni
        exons = feat_dict[key]
        # rovo la lista delle sequenze primarie degli esoni
        # se negativo inverto
        exon_seq = [rev_comp(fasta_seq[exon[0]-1:exon[1]]) for exon in exons] if strand_dict[gene_id] == '-' else [
            fasta_seq[exon[0]-1:exon[1]] for exon in exons]
        # converto in string
        tr_str = ''.join(exon_seq)
        # Stampo in output l'header FASTA del trascritto
        out.write('\n>/source='+ref_id+' '+'/gene_id='+gene_id+' '+'/transcript_id='+transcript_id+' ' +
                  '/type=transcript'+' '+'/length='+str(len(tr_str))+' '+'/strand='+strand_dict[gene_id] + '\n')
        # Stampo in output il trascritto separato in pezzi di 80bp
        # print(split_string(tr_sequence, 80, '\n'))
        out.write('\n'.join([tr_str[i:i+80]
                             for i in range(0, len(tr_str), 80)]))

# rifaccio per cds
for key in feat_dict:
    if key.split('$')[0] == 'CDS':
        cdss = feat_dict[key]
        cds_seq = [rev_comp(fasta_seq[cds[0]-1:cds[1]]) for cds in cdss] if strand_dict[gene_id] == '-' else [
            fasta_seq[cds[0]-1:cds[1]] for cds in cdss]
        # converto in string
        cds_str = ''.join(cds_seq)
        # check start codon stop codonz
        start = 'YES' if cds_str[0: 3] in ['ATG', 'atg'] else 'NO'
        stop = 'YES' if cds_str[len(cds_str)-3: len(cds_str)] in [
            'TAG', 'TAA', 'TGA', 'tag', 'taa', 'tga'] else 'NO'
        # stampo
        out.write('\n>/source='+ref_id+' '+'/gene_id='+gene_id+' '+'/transcript_id='+transcript_id+' '+'/type=cds'+' '+'/length=' +
                  str(len(cds_str))+' '+'/strand='+strand_dict[gene_id]+' '+'/start_codon='+start+' '+'/stop_codon='+stop + '\n')
        out.write('\n'.join([cds_str[i:i+80]
                             for i in range(0, len(cds_str), 80)]))
