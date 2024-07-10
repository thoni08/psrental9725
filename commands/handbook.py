import discord
from discord.ext import commands
from os.path import basename

class Handbook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{basename(__file__)} ready.")

    @discord.app_commands.command(name="help")
    async def help(self, interaction: discord.Interaction) -> None:
        embed=discord.Embed()
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Handbook(bot))