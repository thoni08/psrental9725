import discord
import os
from datetime import datetime, timedelta
from discord.ext import commands
from discord.utils import format_dt, utcnow

class VC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} ready.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        time = (utcnow() + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")

        if not before.channel and after.channel:
            print(f'[{time}] {member} joined the "{after.channel}" voice channel')

        elif before.channel and not after.channel:
            print(f'[{time}] {member} left the "{before.channel}" voice channel')

async def setup(bot):
    await bot.add_cog(VC(bot))