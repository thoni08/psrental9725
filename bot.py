import asyncio
import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from os.path import join, dirname

load_dotenv(join(dirname(__file__), '.env'))

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all(), application_id=os.getenv('APP_ID'))
    
    async def setup_hook(self):
        print("Importing commands...")
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                await self.load_extension(f'commands.{filename[:-3]}')

        print("Importing events...")
        for filename in os.listdir('./events'):
            if filename.endswith('.py'):
                await self.load_extension(f'events.{filename[:-3]}')
        
        # self.tree.copy_global_to(guild=discord.Object(id=os.getenv('GUILD_ID')))
        await self.tree.sync(guild=discord.Object(id=os.getenv('GUILD_ID')))

    async def on_ready(self):
        await self.wait_until_ready()
        print(f"Bot ready. Currently using {discord.__version__}")

Bot().run(os.getenv('TOKEN'))