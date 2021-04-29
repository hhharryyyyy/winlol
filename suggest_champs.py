import json
import pprint
import math

with open('champions.json') as f:
    champs = json.load(f)
with open('winrates_mid.json') as f:
    wr_dict = json.load(f)

def num_of_games(id):
    out = 0
    for _, c in wr_dict[id].items():
        out+=c['n']
    return out

def build_matchup_dict(champ_list):
    out = {}
    for c in champ_list:
        # print("************* build match up dict for ",c, champs[c])
        matchup_dict = build_matchup_dict_for_champ(c)
        if not out:
            out = matchup_dict
        else:
            temp = {}
            for d in (out, matchup_dict):
                for k, v in d.items():
                    temp.setdefault(k, float('-inf'))
                    temp[k] = max(temp[k], v)
            out = temp
    return out 

def build_matchup_dict_for_champ(id):
    out = {}
    if id == 41:
        print("this is gp")
    matchups = wr_dict[id]
    for id2, matchup in matchups.items():
        if matchup['n'] < 100:
            continue
        # bigger number means more  winning with more certainty
        p = num_of_games(id)
        s = matchup['n']
        # w = (matchup['delta2'] + 25) * 2
        w = matchup['wr']
        if w < 0:
            w = 1
        if w > 100:
            w = 99
        out[id2] = math.sqrt(3.8416 * (w/100) * (1-(w/100)) / s * ((p-s)/(p-1))) * 100
        if id == "41":
            print(champs[id2], out[id2], s, w)
    return out

sorted_champs = sorted(champs.items(), key=lambda x: x[1])
pp = pprint.PrettyPrinter(indent = 4)
pp.pprint(sorted_champs)

def champ_pool_score(matchup_dict):
    return sum(matchup_dict.values())


# input_string = input('Enter space separated champ ids:')
# user_list = input_string.split()


# for i in range(len(user_list)):
#     if i not in champs.keys():
#         print('bad input')
#         quit() 
# print('list: ', user_list)
user_list = ['55', '80' ]
matchup_dict = build_matchup_dict(user_list)
print('champ_pool_score: ', champ_pool_score(matchup_dict))


# sorted_matchup = sorted(matchup_dict.items(), key=lambda x: x[1])
# for k, v  in sorted_matchup:
#     print(champs[k], v)

champ_rec_dict = {}
for k in champs.keys():
    print(champs[k])
    d = build_matchup_dict(user_list + [k])
    s = champ_pool_score(d)
    champ_rec_dict[k] = s
    print(user_list + [k], s)


champ_rec_dict = sorted(champ_rec_dict.items(), key=lambda x: x[1])
for k, v  in champ_rec_dict:
    print(champs[k], v)
