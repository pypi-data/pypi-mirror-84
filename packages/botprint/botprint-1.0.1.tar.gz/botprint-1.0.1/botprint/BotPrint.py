"""
Usage: \n
update environment Variables in TOKEN.env in for example .../Python/Python37/Lib/site-packages/Bot_Print \n
PRINTER_TOKEN = your Discord-Bot Token \n
DISCORD_GUILD = the Standard Guild you want to use (you can call it manualy in the functions if you want) \n
DISCORD_CHANNEL = the Standard Cannel in your Guild you want to use ("") \n
\n
finaly just import Bot_Print.bprint as bprint and have fun \n
\n
Functions: \n
tostring(Array): Converts Python-Array into String \n
splitString(STRING): Splits String in Strings of length 2000 which is the Maximum String-Size in Discord \n
bprint(Object, guild=GUILD, Channel=CHANNEL): converts some stuff and prints out x in given channel \n
def shutdown(): closes bot-event-loop (should always be called at the end of the program) \n
"""

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from threading import Thread
import asyncio
import numpy as np

TOKEN_PATH = "./TOKEN.env"
load_dotenv(TOKEN_PATH)
TOKEN = os.getenv('PINTER_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')
bot = commands.Bot(command_prefix='/')
botloop = asyncio.get_event_loop()
is_ready = False


def tostring(Array):
	"""
	Converts Python-Array into String
	"""
	array = []
	array = Array
	for i, element in enumerate(array):
		array[i] = str(element)

	return "[" + ", ".join(array) + "]"

def splitString(STRING):
	"""
	Splits String in Strings of length 2000 which is the Maximum String-Size in Discord \n
	returns 1D Array containing the splitted Strings
	"""
	erg = []
	for i in range(0, int(len(STRING)/2000)+1):
		erg.append(STRING[i*2000:(i+1)*2000])
	return erg


def bprint(Object, guild=GUILD, Channel=CHANNEL ):
	"""	
	converts some stuff and prints out x in given channel \n
	Object: array, ndarray, Any with str() convertable Object \n
	guild : str \n
	Channel : str
	"""

	Type = type(Object)
	if Type is list:
		Message = tostring(Object)
	elif Type is np.ndarray:
		Message = tostring(Object.tolist())
	else: Message = str(Object)
	for i in splitString(Message):
		PRINT(i, guild=guild, Channel=Channel)

def PRINT(x, guild=GUILD, Channel=CHANNEL):
	"""
	prints out x in given channel \n
	x must be convertable to String \n
	guild : str \n
	Channel : str
	"""
	guild = discord.utils.get(bot.guilds, name=GUILD)
	channel = discord.utils.get(guild.channels, name=Channel)
	
	Message = str(x)

	send_fut = asyncio.run_coroutine_threadsafe(channel.send(Message), botloop)
	send_fut.result()

def shutdown():
	"""
	closes bot-event-loop (should always be called at the end of the program)
	"""
	# send_fut = asyncio.run_coroutine_threadsafe(bot.logout(), botloop)
	botloop.create_task(bot.logout())	
	print("Bot has logged out")

def run_bot():
	try:
		botloop.run_until_complete(bot.start(TOKEN))
	except KeyboardInterrupt:
		botloop.run_until_complete(bot.logout())
		# cancel all tasks lingering
	finally:
		botloop.close()


@bot.event
async def on_ready():
	global is_ready
	game = discord.Game("/bip to check activity")
	await bot.change_presence(activity=game)
	print(f'{bot.user.name} has connected to Discord!')
	is_ready = True

@bot.command(name='bip', help='bop')
async def bip(ctx):
	await ctx.send('bop')

BOT_THREAD = Thread(target=run_bot)
BOT_THREAD.start()
while not is_ready:
	None