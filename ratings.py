import string
import urllib.request, urllib.error
from bs4 import BeautifulSoup

def rating(title, type='all'): 
	header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',}
	meta_url = 'http://www.metacritic.com/search/{}/{}/results'.format(type, title.lower().replace(" ", '%20'))	
	meta = urllib.request.Request(meta_url, None, header)
	try:
		with urllib.request.urlopen(meta) as meta_req:
			meta_soup = BeautifulSoup(meta_req.read(), 'html.parser')
			return grab_rating_meta(meta_soup)	
	except urllib.error.URLError as e:
		return e.reason

def grab_rating_meta(meta_soup):
	meta_match = meta_soup.find('h3')
	if meta_match is not None:
		while(True):
			if meta_match.find_next('span').get_text().isdigit():
				return 	meta_match.get_text() + " has a Metacritic score of " + meta_match.find_next('span').get_text() + '%'
			meta_match = meta_match.find_next('h3')
			if meta_match is None: break
	return 'Score not found on Metacritic'