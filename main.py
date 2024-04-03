import os
import discord
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()
intents.members = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print("Ready!")

cogs_list = [
    'nfd_role'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

bot.run(DISCORD_TOKEN)
