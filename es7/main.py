import re
# funzioni check e count descritte sotto


def check(value, dictionary):
    for elem in dictionary["@PG"]:
        if elem[0][1] == value.split(':')[2]:
            return elem[1][1]


def count(str):
    return sum([int(elem[:-1]) for elem in re.findall('([0-9]+M)', str)])


with open('input.sam', 'r') as file:
    sam = [line.strip().split() for line in file.readlines()]

out = open('output.txt', 'w')
headers = [[elem[0]] + [elem[i].split(':')
                        for i in range(1, len(elem))]
           for elem in [elem for elem in sam if elem[0][0] == '@']]

dictionary = {}
# creo dizionario dei vari header @
for elem in headers:
    if elem[0] not in dictionary:
        dictionary[elem[0]] = elem[1:]
    else:
        # funziona solo così, mistero
        back = [dictionary[elem[0]]]
        back.append(elem[1:])
        dictionary[elem[0]] = back

# idem come sopra ma per i !=@
values = [[elem[0]] + [elem[i]
                       for i in range(1, len(elem))] for elem in [elem for elem in sam if elem[0][0] != '@']]

# stampo
out.write(
    '\t'.join(['Read', 'Reference', 'Software', 'Position', '\#Matches']))
out.write('\n')
# read, references e position già in value
# software cerco nel dizionario il tezo elemento dell'ultima stringa dei value (P1 o P2)
# e rendo il nome del software in corrispondenza nel dizionario
# esempio ho ['ID', 'P2'], ['PN', 'BWA']] e cerco P2 esce BWA
# per i march prendo la string in posizione 6 e sommo le cifre antecedenti la M
# per esempio con 8M2I4M1D3M sommo 8+4+3 = 15
for elem in values:
    out.write(elem[0] + '\t' + elem[2] + '\t\t' +
              str(check(elem[-1], dictionary)) + '\t\t' + elem[3] +
              '\t\t' + str(count(elem[5])) + '\n')
