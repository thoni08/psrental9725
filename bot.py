import asyncio
import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from os.path import join, dirname

load_dotenv(join(dirname(__file__), '.env'))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Bot ready. Currently using {discord.__version__}")

bot.run(os.getenv('TOKEN'))