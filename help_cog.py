import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.help_message = """
```
Commands:
?help - dislpays all the commands for yall
?p <keywords> - finds the songs on youtube (better than other dogshit bots)
?q - shows the queue
?skip - skips song
?clear - clears queu
?leave - disconnects bot from vc
?pause - Take a guess what this does
?resume - resumes playing the current song
```
"""
        self.text_channel_text = []
    '''
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            for channel in guild.text_channels:
                self.text_channel_text.append(channel)
                
        await self.send_to_all(self.help_message)

    async def send_to_all(self, msg):    
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)

        
    @commands.command(name="help", help="helps you ... probably")
    async def help(self, ctx):
        await ctx.send(self.help_message)
    '''