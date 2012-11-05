#!/usr/bin/python

import re
from urllib3 import HTTPConnectionPool
from datetime import date,timedelta
from bs4 import BeautifulSoup

months = {
	'Aug' : '8/',
	'Sep' : '9/',
	'Oct' : '10/',
	'Nov' : '11/',
	'Dec' : '12/',
	'Jan' : '1/',
	'Feb' : '2/'
}

todayformat = date.today().strftime('%Y%m%d')
re_proc = re.compile("Processed$")
re_add = re.compile("(Add$|Add \(Waivers\)$)")
pool = HTTPConnectionPool('games.espn.go.com', maxsize=100)

for league in range(75000,150000):
	
	r = pool.request('GET', '/ffl/recentactivity', fields={'leagueId':league, 'seasonId':'2012', 'activityType':'2', 'startDate':'20120901', 'teamId':'-1', 'tranType':'-3'})
	pagesoup = BeautifulSoup(r.data)	
	
	if pagesoup.find_all(text=re_proc):
		l = pool.request('GET', '/ffl/leaguesetup/settings', fields={'leagueId':league})
		if 'Each reception' in l.data:
			league_type = 'PPR'
		else:
			league_type = 'Standard'

		for trade in pagesoup.find_all(text=re_proc):
			tradeinfo = trade.find_parent("td").next_sibling
			dateinfo = trade.find_parent("td").previous_sibling
			tradedate = months[dateinfo.contents[0].split(', ')[1].split()[0]] + dateinfo.contents[0].split(', ')[1].split()[1]
			
			#playerlist1,playerlist2,playerlist1drop,playerlist2drop = [],[],[],[]
			playerlist1,playerlist2 = [],[]
			team = ''
			
			for player in tradeinfo.find_all('b'):
				if team == '':
					team1 = player.previous_sibling.split()[0]
				if player.previous_sibling.split()[0] == team1:
					if player.previous_sibling.split()[-1] == 'traded':
						playerlist1.append(player.next_element)
						team = team1
					#else:
					#	playerlist1drop.append('--' + player.next_element)
					#	team = team1
				else:
					team2 = player.previous_sibling.split()[0]
					if player.previous_sibling.split()[-1] == 'traded':
						playerlist2.append(player.next_element)
						team = team2
					#else:
					#	playerlist2drop.append('--' + player.next_element)
					#	team = team2

			if (len(playerlist1) > len(playerlist2)):
				i = len(playerlist1) - len(playerlist2)
				for sib in tradeinfo.find_all_previous(text=re_add):
					sibtext = sib.find_parent("td").next_sibling
					if re.search('^' + team1, sibtext.text):
						playerlist2.append('++' + sibtext.find('b').text)
						i -= 1
					if i == 0:
						break

			elif (len(playerlist2) > len(playerlist1)):
				i = len(playerlist2) - len(playerlist1)
				for sib in tradeinfo.find_all_previous(text=re_add):
					sibtext = sib.find_parent("td").next_sibling
					if re.search('^' + team2, sibtext.text):
						playerlist1.append('++' + sibtext.find('b').text)
						i -= 1
					if i == 0:
						break
	
			#players1 = ','.join(playerlist1 + playerlist2drop)
			#players2 = ','.join(playerlist2 + playerlist1drop)
			
			players1 = ','.join(playerlist1)
			players2 = ','.join(playerlist2)

			week = int((date(2012,int(tradedate.split("/")[0]),int(tradedate.split("/")[1])) - timedelta(days=2)).strftime('%U')) - 35
			
			if (len(players1) > 0 and len(players2) > 0):
				print "%d|%s|%s|%d|%s|%s" % (league,league_type,tradedate,week,players1,players2)
