import discord
from discord.ext import commands
from datetime import datetime, time, timedelta
import asyncio
import requests

f = open('creds.txt','r')
creds = f.read()

 # look at grabfreegames.com and grab games
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://grabfreegames.com/"

try:
   page = urlopen(url)
except:
   print("Error opening the URL")

soup = BeautifulSoup(page, 'html.parser')

content = soup.find('div', {"class": "freebies row break-on-4"})

result = ''
for i in content.findAll('div'):
    for x in i.findAll('div', {"class": "free-title"}):
        for a in x.findAll('a', href=True):
            if 'Free Steam Game' in x.text:
                result = result + ' ' +  x.text + '    -    ' + str(a['href'])
            if 'Free Epic Games Game' in x.text:
                result = result + ' ' +  x.text + '    -    ' + str(a['href'])
            if 'Free GOG Game' in x.text:
                result = result + ' ' +  x.text + '    -    ' + str(a['href'])

print(result)

###########


# discord creds
TOKEN = str(creds)

from discord.ext import commands, tasks

bot = commands.Bot("!")

target_channel_idXOX = 939170953290719322
target_channel_idMIN = 936999636625940540
##############


@tasks.loop(hours=168)
async def called_once_a_dayXOX():
    message_channel = bot.get_channel(target_channel_idXOX)
    print(f"Got channel {message_channel}")
    await message_channel.send(result)

@tasks.loop(hours=168)
async def called_once_a_dayMIN():
    message_channel = bot.get_channel(target_channel_idMIN)
    print(f"Got channel {message_channel}")
    await message_channel.send(result)

@called_once_a_dayXOX.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")

@called_once_a_dayMIN.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")

called_once_a_dayXOX.start()
called_once_a_dayMIN.start()
bot.run(TOKEN)