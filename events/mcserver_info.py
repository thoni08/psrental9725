import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from exaroton import Exaroton
from os.path import join, dirname

load_dotenv(join(dirname(__file__), '.env'))
exaroton = Exaroton(os.getenv('MCTOKEN'))
    
def embed(server_info):
    if server_info.status == 'Online':
        color = discord.Color.green()
        name = "Online Players"
        value = f"{server_info.players.count}"
    
    if server_info.status == 'Offline':
        color = discord.Color.red()
        name = "Currently Offline"
        value = ""

    embed=discord.Embed(title="Kondisi Server Minecraft", color=color)
    embed.add_field(name="Server Address", value=f"{server_info.address}", inline=True)
    embed.add_field(name="Port", value=f"{server_info.port}", inline=True)
    embed.add_field(name=name, value=value, inline=False)
    embed.add_field(name="", value="[auto add ke mc](https://add.exaroton.com/duniapsrental)", inline=True)
    
    return embed

class Button(discord.ui.View):
    @discord.ui.button(label="▶ Start Server", style=discord.ButtonStyle.green)
    async def start_server(self, interaction: discord.Interaction, button: discord.ui.Button):
        exaroton.start(os.getenv('MC_SERVER_ID'))
        await interaction.response.send_message("Server starting.", ephemeral=True)

        self.stop()

class MCServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} ready.")

        channel = self.bot.get_channel(int(os.getenv('MC_UPDATES_ID')))
        message = await discord.utils.get(channel.history(limit=5), author=self.bot.get_user(int(os.getenv('APP_ID'))))

        while True:
            server_info = exaroton.get_server(os.getenv('MC_SERVER_ID'))

            if message != None:
                if server_info.status == 'Offline':
                    await message.edit(embed=embed(server_info), view=Button())
                else:
                    await message.edit(embed=embed(server_info), view=None)
            else:
                if server_info.status == 'Offline':
                    message = await channel.send(embed=embed(server_info), view=Button())
                message = await channel.send(embed=embed(server_info), view=None)
            
            await asyncio.sleep(60)
                
async def setup(bot):
    await bot.add_cog(MCServerInfo(bot))