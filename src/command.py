# INTERLOCK KNOWLEDGEBASE DISCORD BOT

# include utility functions
import utility

# include others
import os
import discord
import requests
from dotenv import load_dotenv
from github import Github
from discord.ext import commands
#from lib.globs import Git, Mgr

# PAT from blairmunroakusa for dev purposes
# scope restricted to only access public repo info
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
g = Github(GITHUB_TOKEN)

# define and get repo
repo = 'World-Peace-Labs/testee'
repofull = 'https://github.com/' + repo
kb = g.get_repo(repo)




# pipe ls to grep
async def ls_pipe_grep(message):

    # get correlative and keyphrase
    # correl = message.content.replace('kb ls ', '')
    correl, delimit, keyphrase = message.content.replace('kb ls ', '').partition(' | grep ')

    print(correl)
    print(keyphrase)
    # command is: kb-ls --what | grep keyword
    # kb ls what | grep keyword





# bash-style ls command
async def ls(message):

    # get correlative and initiate files list
    correl = message.content.replace('kb ls ', '')
    files: list = []
    
    # get file contents and return error if no file or directory exists
    try:
        for content in kb.get_contents(correl):
            files.append(f'[{content.name}]({repofull}/blob/master/{correl}/{content.name})')
    except:
        await message.reply('Something catastrophic happened and I couldn\'t list the files you requested.')
        return

    # join into single chunk
    files = '\n'.join(files)

    # chunk and send as embed object
    for chunk in utility.chunkstring(files, 4096): # max message reply string length is 4096 char
        embed = discord.Embed(
            title = f'{correl} ls:',
            description = chunk,
        )
        await message.reply(embed=embed)

    return







# ls command switch help
async def ls_help(message):
    
    # get file contents and return error if no file or directory exists
    try:
        kbdata = kb.get_contents(message.content.replace('kb ls help ', '') + '/README.md')
    except:
        await message.reply('ls: *' +
            message.content.replace('kb ls help ', '') +
            '*: no such interrogative correlative.')
        return

    # decode file contents and return error if input is actually directory
    content = kbdata.decoded_content

    # parse decoded content and condition for chat output

    # put into form that will display lines properly
    lines = content.splitlines()

    # strip off all the markdown/html artifacts
    lines = [ str(line).strip('b\'"!') for line in lines ]

    # deal with nonexistant discord markdown headers
    i = 0
    for line in lines:
        if str(line).startswith('##### '):
            lines[i] = line.replace('##### ', '_') + '_'
        if str(line).startswith('#### '):
            lines[i] = line.replace('#### ', '__') + '__'
        if str(line).startswith('### '):
            lines[i] = line.replace('### ', '***') + '***'
        if str(line).startswith('## '):
            lines[i] = line.replace('## ', '**') + '**'
        if str(line).startswith('# '):
            lines[i] = line.replace('# ', '__**') + '**__'
        i += 1 

    # create a single formatted text piece
    joinedlines = '\n'.join(lines)

    # expand relative links into absolute links
    joinedlines = joinedlines.replace(']( ', '](' + repofull + '/blob/master/')

    # expand relative links into absolute links
    joinedlines = joinedlines.replace('](.', '](' + repofull + '/blob/master')

    # eliminate link previews in chat
    joinedlines = joinedlines.replace('](', '](<')

    # chunk and send as embed object
    stringchunks = utility.chunkstring(joinedlines, 4096)
    i = 1
    chunkno = len(list(stringchunks))
    for chunk in utility.chunkstring(joinedlines, 4096): # max message reply string length is 4096 char
        embed = discord.Embed(
            title = f'{kbdata.name} _page {i}/{chunkno}_',
            description = chunk,
        )
        i += 1
        await message.reply(embed=embed)

    return






# bash-style cat command
async def cat(message):

    # get file contents and return error if no file or directory exists
    try:
        kbdata = kb.get_contents(message.content.strip('kb cat '))
    except:
        await message.reply('cat: *' +
            message.content.replace('kb cat ', '') +
            '*: no such markdown/text file or directory.')
        return

    # decode file contents and return error if input is actually directory
    try:
        content = kbdata.decoded_content
    except:
        await message.reply('cat: *' +
            message.content.replace('kb cat ', '') +
            '*: is a directory.')
        return

    # parse decoded content and condition for chat output

    # put into form that will display lines properly
    lines = content.splitlines()

    # strip off all the markdown/html artifacts
    lines = [ str(line).strip('b\'"!') for line in lines ]

    # deal with nonexistant discord markdown headers
    i = 0
    for line in lines:
        if str(line).startswith('##### '):
            lines[i] = line.replace('##### ', '_') + '_'
        if str(line).startswith('#### '):
            lines[i] = line.replace('#### ', '__') + '__'
        if str(line).startswith('### '):
            lines[i] = line.replace('### ', '***') + '***'
        if str(line).startswith('## '):
            lines[i] = line.replace('## ', '**') + '**'
        if str(line).startswith('# '):
            lines[i] = line.replace('# ', '__**') + '**__'
        i += 1 

    # create a single formatted text piece
    joinedlines = '\n'.join(lines)

    # expand relative links into absolute links
    joinedlines = joinedlines.replace(']( ', '](' + repofull + '/blob/master/')

    # expand relative links into absolute links
    joinedlines = joinedlines.replace('](.', '](' + repofull + '/blob/master')

    # eliminate link previews in chat
    joinedlines = joinedlines.replace('](', '](<')

    # break content into permittable chunks and reply in chat
    stringchunks = utility.chunkstring(joinedlines, 4096)
    i = 1
    chunkno = len(list(stringchunks))
    for chunk in utility.chunkstring(joinedlines, 4096): # max message reply string length is 4096 char
        embed = discord.Embed(
            title = f'{kbdata.name} _page {i}/{chunkno}_',
            description = chunk,
        )
        i += 1
        await message.reply(embed=embed)
    return
