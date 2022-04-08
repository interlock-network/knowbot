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

repo = 'blairmunroakusa/portfolio'
repofull = 'https://github.com/' + repo
kb = g.get_repo(repo)

def chunkstring(string, length):
    return (string[i:(length + i)] for i in range(0, len(string), length))

# bash-style cat command
async def cat(message):
    # get file contents and return error if no file or directory exists
    try:
        kbdata = kb.get_contents(message.content.strip('kb-cat '))
    except:
        await message.reply('cat: *' +
            message.content.replace('kb-cat ', '') +
            '*: no such markdown/text file or directory.')
        return
    # decode file contents and return error if input is actually directory
    try:
        content = kbdata.decoded_content
    except:
        await message.reply('cat: *' +
            message.content.replace('kb-cat ', '') +
            '*: is a directory.')
        return
    # parse decoded content and condition for chat output
    content = content.splitlines()
    content = '\n'.join(str(x).strip('b\'') for x in content)
    content = content.replace('](.', '](' + repofull + '/tree/master')
    content = content.replace('](', '](<')
    # break content into permittable chunks and reply in chat
    for string in chunkstring(content, 2000): # max message reply string length is 2000 char
        await message.reply(string)
    return

# help man page
async def cat_help(message):
    output = """
KB-CAT      General Commands Manual

NAME
    kb-cat - contatenate and print files

SYNOPSIS
    kb-cat [--help] [file]

DESCRIPTION
    The cat utility reads text or markdown files, writing them to chat. Replies are broken into 2000 character chunks, and this might interfere with markdown formatting, or it might cause a line to be broken in an awkward place. Relative markdown links have been replaced by the absolute url. To prevent previews for all links in chat, the '<' is prepended to each address.

EXAMPLE
    The command:

        kb-cat file1.md

    will print the contents of file1.md to chat.
"""
    await message.reply(output)
    return

# connect kb-bot
@client.event
async def on_ready():
    server = discord.utils.get(client.guilds, name=SERVER)
    print(
        f'{client.user} is connected to server\n'
        f'{server.name}(id: {server.id})'
    )

# listen for messages
@client.event
async def on_message(message):

    # check for cat command to print file
    if (message.content == 'kb-cat' or
        message.content == 'kb-cat ' or
        message.content == 'kb-cat --help'):
        await cat_help(message)
    elif (message.content.startswith('kb-cat ')):
        await cat(message)

# main
client.run(TOKEN)
