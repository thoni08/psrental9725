import discord
import os
import subprocess
from discord.ext import commands
from dotenv import load_dotenv
from os.path import join, dirname, basename

load_dotenv(join(dirname(__file__), '.env'))

class McServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{basename(__file__)} ready.")

    @discord.app_commands.command(name="start", description="Start Minecraft server.")
    async def start(self, interaction: discord.Interaction) -> None:
        p1 = subprocess.Popen("start_server.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
        p2 = subprocess.Popen("start_playit.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
        await interaction.response.send_message("Server starting.")

async def setup(bot):
    await bot.add_cog(McServer(bot))