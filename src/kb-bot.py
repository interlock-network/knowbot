# INTERLOCK KNOWLEDGEBASE DISCORD BOT

# TODO:
# . mention license in header
# x get simple hello world running
# x implement internals to interact with discord chat
# . implement internals to interact with github API

import os

import discord
import requests
from dotenv import load_dotenv
# from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

client = discord.Client()

kb = 'https://api.github.com/users/interlock-network'

def git_api_repolist(arg):
    kbdata = requests.get(kb).json()
    return f'{arg} {kbdata}'

# connect kb-bot
@client.event
async def on_ready():
    server = discord.utils.get(client.guilds, name=SERVER)
    print(
        f'{client.user} is connected to server\n'
        f'{server.name}(id: {server.id})'
    )

@client.event
async def on_message(message):
    """Invoke when a message is received on the server."""
    if (message.content == 'test'):
        await message.reply(git_api_repolist(message.content))

client.run(TOKEN)
