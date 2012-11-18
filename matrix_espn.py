#!/usr/bin/env python

import sys
import numpy as np
from scipy import optimize

resultsfile = sys.argv[1]
f = open(resultsfile, 'r')

#all_trades = np.array([])
all_trades = []
player_list = []

for line in f:
	players1 = line.split("|")[-2].split(",")
	players2 = line.split("|")[-1].strip("\n").split(",")
	
	trade = [0] * len(player_list)
	
	for player in players1:
		if player not in player_list:
			player_list.append(player)
			trade.append(1)
		player_index = player_list.index(player)
		trade[player_index] = 1
	
	for player in players2:
		if player not in player_list:
			player_list.append(player)
			trade.append(-1)
		player_index = player_list.index(player)
		trade[player_index] = -1
	
	all_trades.append(trade)

f.close()

"""
orig_len = len(player_list)

for t in all_trades:
	t.extend([0] * (orig_len - len(t)))


mxcount = 10

z = open(resultsfile, 'r').read()
person_values = {}
for person in player_list:
	person_values[person] = z.count(person)
	
	if person_values[person] < mxcount:
		for t in all_trades:		
			if t[player_list.index(person)] != 0:
				del all_trades[all_trades.index(t)]
"""

zeroes = [0] * len(all_trades)
zeroes.append(100)
all_trades.append([1])
for t in all_trades:
	t.extend([0] * (len(player_list) - len(t)))

#replace above for with this:
#all_trades[-1].extend([0] * (orig_len - 1))

resultset = optimize.nnls(all_trades,zeroes)[0]

##mx = max(resultset)
for player in player_list:
	##print "%s,%s" % (player,resultset[player_list.index(player)] * (100/mx))
	print "%s,%s" % (player,resultset[player_list.index(player)])
	#if resultset[player_list.index(player)] != 0:
		#print "%s,%s,%d" % (player,resultset[player_list.index(player)],person_values[player])

