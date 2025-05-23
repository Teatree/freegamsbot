import discord
import os
import requests
from discord.ext import commands, tasks

# Constants
TOKEN = os.environ['DISCORD_TOKEN']
TARGET_CHANNEL_IDS = [939170953290719322, 936999636625940540]
GAMERPOWER_API_URL = "https://www.gamerpower.com/api/giveaways?type=game"

# Discord bot setup
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

def get_free_game_links():
    try:
        response = requests.get(GAMERPOWER_API_URL)
        response.raise_for_status()
        giveaways = response.json()
    except Exception as e:
        print("Error fetching free games:", e)
        return "⚠️ Error fetching free games."

    result = ""
    for game in giveaways:
        title = game.get("title", "No Title")
        link = game.get("open_giveaway_url", "")
        platform = game.get("platforms", "")
        
        # Optional: skip browser-only or mobile-only games
        if "Steam" in platform or "Epic" in platform or "GOG" in platform:
            result += f"{title} – {link}\n"

    return result.strip() if result else "No free games found today."

@tasks.loop(count=1)
async def do_its_thing():
    await bot.wait_until_ready()

    message = get_free_game_links()

    for channel_id in TARGET_CHANNEL_IDS:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            print(f"Channel ID {channel_id} not found or not accessible")

    await bot.close()

if __name__ == '__main__':
    do_its_thing.start()
    bot.run(TOKEN)
