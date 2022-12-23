from tokenize import Token
import discord
from discord.ext import commands
import music
import help_cog
from dotenv import load_dotenv
import os


load_dotenv()
Token = os.getenv("TOKEN")
client = commands.Bot(command_prefix='?')

client.remove_command("help")

client.add_cog(help_cog.help_cog(client))
client.add_cog(music.music(client))




client.run(Token)