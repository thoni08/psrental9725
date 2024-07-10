import asyncio
import discord
import os
import subprocess
from discord.ext import commands
from dotenv import load_dotenv
from mcstatus import JavaServer
from os.path import join, dirname, basename

load_dotenv(join(dirname(__file__), '.env'))
server = JavaServer.lookup(os.getenv('MC_IP_STATUS'))
started = False

def embed(server_info):
    color = discord.Color.greyple()
    name = ""
    value = ""
    
    if server_info is not None:
        color = discord.Color.green()
        name = "Online Players"
        value = f"{server_info.players.online}/{server_info.players.max}"
    
    if server_info is None:
        color = discord.Color.red()
        name = "Currently Offline"
        value = ""

    embed=discord.Embed(title="Kondisi Server Minecraft", color=color)
    embed.add_field(name="Server IP (Java)", value=os.getenv('MC_IP_DISPLAY_JAVA'), inline=True)
    embed.add_field(name="Port (Java)", value=os.getenv('MC_IP_DISPLAY_JAVA_PORT'), inline=True)
    embed.add_field(name="", value="", inline=True)
    embed.add_field(name="Server IP (Bedrock)", value=os.getenv('MC_IP_DISPLAY_BEDROCK'), inline=True)
    embed.add_field(name="Port (Bedrock)", value=os.getenv('MC_IP_DISPLAY_BEDROCK_PORT'), inline=True)
    embed.add_field(name=name, value=value, inline=False)
    
    return embed

class Button(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=62)
    
    @discord.ui.button(label="▶ Start Server", style=discord.ButtonStyle.green)
    async def start_server(self, interaction: discord.Interaction, button: discord.ui.Button):
        p1 = subprocess.Popen("start_server.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
        p2 = subprocess.Popen("start_playit.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
        global started
        started = True
        await interaction.response.send_message("Server starting.", ephemeral=True)
        print("start server called")
        self.start_server.disabled = True
        self.stop()

class MCServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{basename(__file__)} ready.")

        channel = self.bot.get_channel(int(os.getenv('MC_UPDATES_ID')))
        message = await discord.utils.get(channel.history(limit=2), author=self.bot.get_user(int(os.getenv('APP_ID'))))

        while True:
            try:
                server_info = server.status()
                global started
                started = True
            except:
                server_info = None
                if started is True and "playit.exe" in str(subprocess.check_output('tasklist')):
                    os.system('taskkill /f /im playit.exe')
                    started = False

            if message != None:
                if server_info is None:
                    await message.edit(embed=embed(server_info), view=Button())
                else:
                    await message.edit(embed=embed(server_info), view=None)
            else:
                if server_info is None:
                    message = await channel.send(embed=embed(server_info), view=Button())
                message = await channel.send(embed=embed(server_info), view=None)
            
            await asyncio.sleep(60)
                
async def setup(bot):
    await bot.add_cog(MCServerInfo(bot))