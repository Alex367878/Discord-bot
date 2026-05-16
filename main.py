import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Botul este online ca {bot.user}!")


async def load_extensions():
    await bot.load_extension("cogs.raiderio")


async def main():
    if not DISCORD_BOT_TOKEN:
        raise ValueError("DISCORD_BOT_TOKEN is missing from .env")

    async with bot:
        await load_extensions()
        print("Starting Discord bot...")
        await bot.start(DISCORD_BOT_TOKEN)


asyncio.run(main())