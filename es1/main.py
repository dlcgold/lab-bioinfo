import numpy as np

with open('./input-precipitazioni.txt', 'r') as f:
    num_cols = len(f.readline().split())

data = np.genfromtxt('./input-precipitazioni.txt', delimiter=None,
                     names=True, usecols=np.arange(1, num_cols + 1))

month = np.genfromtxt('input-precipitazioni.txt',
                      delimiter=None, usecols=0, skip_header=1, dtype=str)


year = np.array(data.dtype.names)

# rendo l'arraydi tuple di genfromtxt un array2d
data_2d = data.view((float, len(data.dtype.names)))

# media mensile
average_month = np.sum(data_2d / len(year), axis=1)

# totale annuo
total_year = np.sum(data_2d, axis=0)

number_rain_year = np.array([])
for i in year:
    number_rain_year = np.append(
        number_rain_year, np.count_nonzero(data[i] > 100))

out = open('./output-precipitazioni.txt', 'w')
out.write("MEDIE MENSILI\n")

for m, a in zip(month, average_month):
    out.write(m[:3].upper() + " => " + str(round(a, 1)) + "\n")

out.write("\nTOTALE ANNUI\n\n")
for y, t in zip(year, total_year):
    out.write(str(y) + " => " + str(int(t)) + "\n")
out.write("\nNUMERO DI MESI PER ANNO CON ALMENO 100 MM DI PIOGGIA\n\n")
for y, n in zip(year, number_rain_year):
    out.write(str(y) + " => " + str(int(n)) + "\n")
