import discord
import asyncio
import markovify
import random
from datetime import datetime as dt
def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

lockoutChannelList = ['lewdzone', 'announcements','snakes-and-stones','robit-test-zone'] #Change or add the names of channels that you do NOT want the bot to auto-copy.

with open("messages.txt") as f: #Change tweets.txt to your source file
    text = f.read()

text_model = markovify.NewlineText(text)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
	if '256830217740484608' in message.content:
		if 'rant' in message.content:
			markovchain = ""
			for i in range(random.randint(1,3)):
				while True:
					try:
						markovchain += text_model.make_sentence() + ' '
						break
					except TypeError:
						print('Value error, retrying...')
			#print(markovchain) #Debug.
			await client.send_message(message.channel, markovchain)
		if 'help' in message.content:
			await client.send_message(message.channel, 'Here is a list of my core functions:' + '\n**Rant** - I will speak my mind' + '\n**Time** - I will tell you the time as it is inside my workshop.')
		if 'time' in message.content:
			await client.send_message(message.channel, 'The current time is ' + dt.now().strftime("%I:%M %p") + ' on ' + custom_strftime("%B the {S}", dt.now()) + ', at least in my workshop. (Eastern Time)')
		if 'archive' in message.content:
			tmp = await client.send_message(message.channel, 'Tabulating...')
			filename = message.author.name + ' ' + dt.now().strftime("%Y.%m.%d %H.%M.%S") + '.txt'
			archive=open(filename, 'w')
			async for log in client.logs_from(message.channel, limit=100):
				if log.author==message.author:
					archive.write(log.clean_content + '\n')
			archive.close()
			await client.edit_message(tmp, 'Tabulation complete, sending...')
			await client.start_private_message(message.author)
			await client.send_file(message.author, filename)
	elif '137099198444208128' in message.author.id:
		ignoreMessage = False
		if 'https://' or 'http://' in message.content:
			print('Link ignored.')
			ignoreMessage = True
		for i in lockoutChannelList:
			if message.channel.name == i:
				print('Message from channel ' + i + ' ignored.')
				ignoreMessage = True
		if ignoreMessage == False:
			if len(message.clean_content) > 0:
				nagaArchive = open('nagaarchive.txt', 'a+')
				nagaArchive.write(message.clean_content + '\n')
				nagaArchive.close()
client.run('MjU2ODMwMjE3NzQwNDg0NjA4.CyyfTQ.jYE0TboYMuRwzff4XU5oBPvAv5c')