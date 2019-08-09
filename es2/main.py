import numpy as np
import sys
from collections import Counter


n = int(sys.argv[1])
data = np.genfromtxt('./atp_matches_2016.csv',
                     delimiter=',', names=True, encoding=None, dtype=None)
headers = data.dtype.names
count = 0

finalist = []
for game in data:
    if game['round'] == 'F':
        finalist.append(
            (game['winner_id'], game['winner_name'], game['winner_hand']))

count = Counter(finalist)
out = open('report-atp-matches.txt', 'w')
for player in count.most_common()[:n]:
    out.write(player[0][1] + ' (' + player[0][2] + ')' +
              ' --> ' + str(player[1]) + '\n')
