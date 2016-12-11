import discord
import asyncio
from markov import markovGen
import random
import pytz
from datetime import datetime,timedelta

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def rollDie(number):
    for i in range(number):
        roll = random.randint(1,20)
    return roll
	
lockoutChannelList = ['lewdzone', 'announcements','snakes-and-stones','robit-test-zone'] #Change or add the names of channels that you do NOT want the bot to auto-copy.

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
	if client.user.id in message.content:
		if 'rant' in message.content:
			await client.send_message(message.channel, markovGen('naga'))
		if 'help' in message.content:
			await client.send_message(message.channel, 'Here is a list of my core functions:' + '\n**Rant** - I will speak my mind.' + '\n**Time** - I will tell you the time as it is inside my workshop.' + '\n**rtd** - I will roll a 20-sided die for you (like I dont have anything better to do.)')
		if 'time' in message.content:
			await client.send_message(message.channel, 'The current time is ' + datetime.now().strftime("%I:%M %p") + ' on ' + custom_strftime("%B the {S}", datetime.now()) + ', at least in my workshop (Eastern Time).')
		if 'rtd' in message.content:
			await client.send_message (message.channel, rollDie(1))
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
		for i in lockoutChannelList:
			if message.channel.name == i:
				print('Message from channel ' + i + ' ignored.')
				ignoreMessage = True
		if ('https://' or 'http://') in message.content:
			print('Link ignored.')
			ignoreMessage = True
		if ignoreMessage != True:
			if len(message.clean_content) > 0:
				nagaArchive = open('nagaarchive.txt', 'a+')
				nagaArchive.write(message.clean_content + '\n')
				nagaArchive.close()
client.run('MjU2ODMwMjE3NzQwNDg0NjA4.CyyfTQ.jYE0TboYMuRwzff4XU5oBPvAv5c')
