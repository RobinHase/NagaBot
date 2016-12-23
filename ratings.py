import random
import re
import string
import urllib.request, urllib.error

from bs4 import BeautifulSoup

def rating(title='freddy got fingered', type='all'): 
	header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',}
	if 'mystery' in type:
		meta_url = 'http://www.metacritic.com/search/popular?page={}'.format(random.randint(0,49))
		meta = urllib.request.Request(meta_url, None, header)
		try:
			with urllib.request.urlopen(meta) as meta_req:
				meta_soup = BeautifulSoup(meta_req.read(), 'html.parser')
		except urllib.error.URLError as e:
			return e.reason
		return grab_rating_random(meta_soup)
	else:
		meta_url = 'http://www.metacritic.com/search/{}/{}/results'.format(type, title.lower().replace(" ", '%20'))	
		meta = urllib.request.Request(meta_url, None, header)
		try:
			with urllib.request.urlopen(meta) as meta_req:
				meta_soup = BeautifulSoup(meta_req.read(), 'html.parser')
		except urllib.error.URLError as e:
			return e.reason
		return grab_rating_game(meta_soup) if 'game' in type else grab_rating_all(meta_soup)
	
def grab_rating_all(meta_soup):
	meta_match = meta_soup.find('h3')
	while meta_match is not None:
		if meta_match.find_next('span').get_text().isdigit() and 'Game' in meta_match.find_previous('strong').get_text():
			return (meta_match.get_text() + ' (' + meta_match.find_previous('span').get_text()
				+ ') has a Metacritic score of ' + meta_match.find_next('span').get_text() +'%')
		elif meta_match.find_next('span').get_text().isdigit():
			return meta_match.get_text() + " has a Metacritic score of " + meta_match.find_next('span').get_text() + '%'
		meta_match = meta_match.find_next('h3')
		if meta_match is None: break
	return 'Score not found on Metacritic'

def grab_rating_game(meta_soup):
	meta_match = meta_soup.find('h3')
	if meta_match is not None: first_result = meta_match.get_text() 
	is_first_result = False
	meta_game = []
	while meta_match is not None:
		if meta_match.find_next('span').get_text().isdigit() and 'Game' in meta_match.find_previous('strong').get_text() and meta_match.get_text() == first_result:
			is_first_result = True
			meta_game.append(meta_match.get_text() + ' (' + meta_match.find_previous('span').get_text() 
				+ ') has a Metacritic score of ' + meta_match.find_next('span').get_text() +'%')
		meta_match = meta_match.find_next('h3')
		if not is_first_result: first_result = meta_match.get_text()
		if meta_match is None: break
		
	i = 0
	low = 100
	high = 0
	highest_score = 'Wadda hell......bulnosaur'
	while i < len(meta_game):
		if int(re.findall('\d+', meta_game[i])[-1]) >= high:
			high = int(re.findall('\d+', meta_game[i])[-1])
			highest_score = meta_game[i]
		if int(re.findall('\d+', meta_game[i])[-1]) <= low:
			low = int(re.findall('\d+', meta_game[i])[-1])
		i += 1
		
	if high - low >= 10:
		meta_game.sort(key=lambda x:int(x.split()[-1].replace('%','')), reverse=True)
		return 'Score not found on Metacritic' if not meta_game else ', '.join(meta_game)
	else:
		return 'Score not found on Metacritic' if not meta_game else highest_score
	
def grab_rating_random(meta_soup):
	meta_match = meta_soup.find('h3')
	if meta_match is not None: first_result = meta_match.get_text() 
	meta_rand = []
	while meta_match is not None:
		if meta_match.find_next('span').get_text().isdigit() and 'Game' in meta_match.find_previous('strong').get_text():
			meta_rand.append('Random ' + meta_match.find_previous('strong').get_text().lower() +' review: ' 
			+ meta_match.get_text() + ' (' + meta_match.find_previous('span').get_text() + ') '+ meta_match.find_next('span').get_text() +'%')
		elif meta_match.find_next('span').get_text().isdigit():
			meta_rand.append('Random ' + meta_match.find_previous('strong').get_text().lower() +' review: ' 
			+ meta_match.get_text() + ' ' + meta_match.find_next('span').get_text() +'%')
		meta_match = meta_match.find_next('h3')
		if meta_match is None: break
	return 'Issue pulling score from page. Please try again.' if not meta_rand else meta_rand[random.randint(0,len(meta_rand) - 1)]
		
	
