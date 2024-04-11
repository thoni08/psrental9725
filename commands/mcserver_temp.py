import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from exaroton import Exaroton
from os.path import join, dirname

load_dotenv(join(dirname(__file__), '.env'))
exaroton = Exaroton(os.getenv('MCTOKEN'))

class McServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} ready.")

    @discord.app_commands.command(name="start", description="Start Minecraft Exaroton server.")
    async def start(self, interaction: discord.Interaction) -> None:
        exaroton.start(os.getenv('MC_SERVER_ID'))
        await interaction.response.send_message("Server starting.")

async def setup(bot):
    await bot.add_cog(McServer(bot))