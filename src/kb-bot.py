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
from github import Github
from pprint import pprint
# from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

client = discord.Client()

# PAT from blairmunroakusa for dev purposes
# scope restricted to only access public repo info
g = Github('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')

kb = g.get_repo('blairmunroakusa/portfolio')

# interlock = Github().get_user('interlock-network')

class Content:
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return fr'{self.content}'

def print_content(arg):
    kbdata = kb.get_contents('README.md')
    # kbdata = interlock.get_repos()
    # kbdata = requests.get('https://api.github.com/users/interlock-network').json()
    # content = Content(kbdata.decoded_content)
    test = 'testee1\n' + 'testee2\n'
    test2 = kbdata.decoded_content
    return f"""{arg} {kbdata.html_url}
{test2}
"""
    # return print(f'testee\n' f'testtwo')

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
        await message.reply(print_content(message.content))

client.run(TOKEN)
