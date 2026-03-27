import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv() 
API_KEY = os.getenv("WEATHER_API_KEY") 
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Botul este online!")

async def load():
    await bot.load_extension("cogs.raiderio") 

async def main():
    async with bot:
        await load()
        print("Start discord bot token" + DISCORD_BOT_TOKEN)
        await bot.start(DISCORD_BOT_TOKEN)

asyncio.run(main())

