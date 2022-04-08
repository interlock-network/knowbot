# INTERLOCK KNOWLEDGEBASE DISCORD BOT

# include utility functions
import utility

# include others
import os
import discord
import requests
from dotenv import load_dotenv
from github import Github

# PAT from blairmunroakusa for dev purposes
# scope restricted to only access public repo info
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
g = Github(GITHUB_TOKEN)

# define and get repo
repo = 'blairmunroakusa/portfolio'
repofull = 'https://github.com/' + repo
kb = g.get_repo(repo)

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

    # put into form that will display lines properly
    content = content.splitlines()
    content = '\n'.join(str(x).strip('b\'') for x in content)

    # expand relative links into absolute links
    content = content.replace('](.', '](' + repofull + '/tree/master')

    # eliminate link previews in chat
    content = content.replace('](', '](<')

    # break content into permittable chunks and reply in chat
    for string in utility.chunkstring(content, 2000): # max message reply string length is 2000 char
        await message.reply(string)
    return
