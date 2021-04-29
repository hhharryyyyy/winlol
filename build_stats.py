# https://apix1.op.lol/mega/?ep=champion&p=d&v=9&patch=11.8&cid=8&lane=default&tier=platinum_plus&queue=420&vs=122&vslane=middle


import json
import urllib.request
import collections
import time


with open('champions.json') as f:
    champs = json.load(f)

champ_ids = champs.keys()
wr_dict = collections.defaultdict(dict)
for id1 in champ_ids:
    for id2 in champ_ids:
        if id1 == id2:
            continue

        url = 'https://apix1.op.lol/mega/?ep=champion&p=d&v=9&patch=11.8&cid={cid}&lane=middle&tier=platinum_plus&queue=420&vs={vsid}&vslane=middle'.format(cid=id1, vsid=id2)
        print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read()
        values = json.loads(data)
        header = values['header']

        if 'wr' not in header or 'delta2' not in header or 'n' not in header:
            print("no data for {c1} vs {c2}".format(c1=champs[id1], c2=champs[id2]))
            continue

        print(id1, id2)
        wr_dict[id1][id2] = {'vslane': 'middle', 'wr': header['wr'], 'delta2': header['delta2'], 'n': header['n']}


with open('winrates_mid.json', 'w') as json_file:
  json.dump(wr_dict, json_file)
