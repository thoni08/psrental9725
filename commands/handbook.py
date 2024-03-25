import discord
import os
from discord import app_commands
from discord.ext import commands

class Handbook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} ready.")

    @discord.app_commands.command(name="help")
    async def help(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("help")

async def setup(bot):
    await bot.add_cog(Handbook(bot))