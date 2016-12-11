###Alkybot Markov Module
###Receives one required string var that determines the database to feed from, and one optional int var that determines the length
###		of string to generate.
###Valid entries for length are 0 through 5. 0 will generate a string of random length, and is the default.
import markovify
import random

def markovGen(database, length=0):
	if 'naga' in database:
		database = 'nagaarchive.txt'
	else:
		database = 'nagaarchive.txt'
	try:
		with open(database) as f:
			text = f.read()
	except FileNotFoundError:
		return 'Dictionary not found!'
	text_model = markovify.NewlineText(text)
	if length == 0:
		length = random.randint(1,5)
	elif length > 5:
		length = 5
	markovChain = ''
	for i in range(length):
		while True:
			try:
				markovChain += text_model.make_sentence() + ' '
				break
			except TypeError:
				return('Something broke. Is the dictionary long enough?')
	return markovChain