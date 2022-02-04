import discord
import random
from epicstore_api import EpicGamesStoreAPI, OfferData
from discord.ext import commands
from datetime import datetime, time, timedelta
import asyncio


epicText = "**EPIC FREE GAMES:** \n" 
url = "x"

combinedTextUrl = ""

api = EpicGamesStoreAPI() 
free_games = api.get_free_games()['data']['Catalog']['searchStore']['elements']
for game in free_games:
    game_name = game['title']
    game_thumbnail = None
    # Can be useful when you need to also show the thumbnail of the game.
    # Like in Discord's embeds for example, or anything else.
    # Here I showed it just as example and won't use it.
    for image in game['keyImages']:
        if image['type'] == 'Thumbnail':
            game_thumbnail = image['url']
    game_price = game['price']['totalPrice']['fmtPrice']['originalPrice']
    #print("GAME PROMOTIONS")
    #print(game)
    try:
        game_promotions = game['promotions']['promotionalOffers']
        upcoming_promotions = game['promotions']['upcomingPromotionalOffers']
        print(bool(upcoming_promotions))
        if bool(upcoming_promotions) == True:
            # Promotion is not active yet, but will be active soon.
            promotion_data = upcoming_promotions[0]['promotionalOffers'][0]
            start_date_iso, end_date_iso = (
                promotion_data['startDate'][:-1], promotion_data['endDate'][:-1]
            )
            # Remove the last "Z" character so Python's datetime can parse it.
            start_date = datetime.fromisoformat(start_date_iso)
            end_date = datetime.fromisoformat(end_date_iso)
            print('{} ({}) will be free from {} to {} UTC.'.format(
                game_name, game_price, start_date, end_date
            ))
        else:
            print('{} ({}) is FREE now.'.format(
                game_name, game_price
            ))
            epicText = epicText + '{} ({}) is FREE now.'.format(
                game_name, game_price
            )
            url = "https://www.epicgames.com/store/en-US/p/" + game['urlSlug']
            print(url)
            
            combinedTextUrl = combinedTextUrl+epicText+"\n"+url
    except TypeError:
        pass


TOKEN = "OTM5MTEzOTQ0ODY4NTg1NTMy.Yf0IBA.DSJCCM3-6B_slBM9ssH7Pa8epC4"

from discord.ext import commands, tasks

bot = commands.Bot("!")

target_channel_idXOX = 939170953290719322
target_channel_idMIN = 936999636625940540

@tasks.loop(hours=168)
async def called_once_a_dayXOX():
    message_channel = bot.get_channel(target_channel_idXOX)
    print(f"Got channel {message_channel}")
    await message_channel.send(combinedTextUrl)

@tasks.loop(hours=168)
async def called_once_a_dayMIN():
    message_channel = bot.get_channel(target_channel_idMIN)
    print(f"Got channel {message_channel}")
    await message_channel.send(combinedTextUrl)

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




# CODE For Custom Commands

#client = discord.Client()
#
#@client.event
#async def on_ready():
#	print("Bitch {0.user}".format(client))
#
#@client.event
#async def on_message(message):
#	username = str(message.author).split('#')[0]
#	user_message = str(message.content)
#	channel = str(message.channel.name)
#	print(f'{username}: {user_message} ({channel})')
#	
#	if message.author == client.user:
#		return
#		
#	if message.channel.name == '🔥free-games':
#		if user_message.lower() == 'hello':
#			await message.channel.send(f'Hello {username}! ' + text + "\n" + url)
#			return
#		elif user_message.lower() == 'bye':
#			await message.channel.send(f'Bye {username}!')
#			return
#		elif user_message.lower() == '!random':
#			response = f'This is your random number: {random.randrange(10000)}'
#			await message.channel.send(response)
#			return
#	
#client.run(TOKEN)