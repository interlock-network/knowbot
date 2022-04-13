# INTERLOCK KNOWLEDGEBASE DISCORD BOT

# include local modules
import utility

# include others
import os
import discord
import requests
from dotenv import load_dotenv
from github import Github

# PAT from blairmunroakusa for dev purposes
# scope restricted to only access public repo info
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
g = Github(GITHUB_TOKEN)

# define and get repo
repo = 'World-Peace-Labs/testee'
repofull = 'https://github.com/' + repo
kb = g.get_repo(repo)



# grep all
async def grep_all(message):

    # initiate files list
    resultlines: list = []

    # get keyphrase
    keyphrase = message.content.replace('kb grep ', '').replace(' *', '')
    print(keyphrase)

    # get file contents and return error if no file or directory exists
    try:
        for correl in utility.correl:
            for content in kb.get_contents(correl):
                lines = content.decoded_content.splitlines()

                # strip off all the markdown/html artifacts
                lines = [ str(line).strip('b\'"!') for line in lines ]
                
                for line in lines:
                    
                    if line.__contains__(keyphrase):

                        # deal with nonexistant discord markdown headers
                        if str(line).startswith('##### '):
                            line = line.replace('##### ', '_') + '_'
                        if str(line).startswith('#### '):
                            line = line.replace('#### ', '__') + '__'
                        if str(line).startswith('### '):
                            line = line.replace('### ', '***') + '***'
                        if str(line).startswith('## '):
                            line = line.replace('## ', '**') + '**'
                        if str(line).startswith('# '):
                            line = line.replace('# ', '__**') + '**__'


    except:
        await message.reply('Something catastrophic happened and I couldn\'t list the files you requested.')
        return


    # join into single chunk
    resultlines = '\n'.join(resultlines)

    # chunk and send as embed object
    i = 1
    chunkno = len(list(utility.embedsplit(resultlines, 4096)))
    for chunk in utility.embedsplit(resultlines, 4096): # max message reply string length is 4096 char
        embed = discord.Embed(
            title = f'grep all \'{keyphrase}\' _page {i}/{chunkno}_:',
            description = chunk,
        )
        await message.reply(embed=embed)
        i += 1

    return





# pipe ls all to grep
async def ls_grep(message):

    # initiate files list
    files: list = []

    # get keyphrase
    keyphrase = message.content.replace('kb ls | grep ', '')

    # get file contents and return error if no file or directory exists
    try:
        for correl in utility.correl:
            for content in kb.get_contents(correl):
                if content.name.__contains__(keyphrase):
                    files.append(f'[{content.name}]({repofull}/blob/master/{correl}/{content.name})')
    except:
        await message.reply('Something catastrophic happened and I couldn\'t list the files you requested.')
        return

    # join into single chunk
    files = '\n'.join(files)

    # chunk and send as embed object
    i = 1
    chunkno = len(list(utility.embedsplit(files, 4096)))
    for chunk in utility.embedsplit(files, 4096): # max message reply string length is 4096 char
        embed = discord.Embed(
            title = f'ls | grep \'{keyphrase}\' _page {i}/{chunkno}_:',
            description = chunk,
        )
        await message.reply(embed=embed)
        i += 1

    return






# pipe ls correl to grep
async def ls_correl_grep(message):

    # get correlative and keyphrase and initiate files list
    correl, delimit, keyphrase = message.content.replace('kb ls ', '').partition(' | grep ')
    files: list = []

    # get file contents and return error if no file or directory exists
    try:
        for content in kb.get_contents(correl):
            if content.name.__contains__(keyphrase):
                files.append(f'[{content.name}]({repofull}/blob/master/{correl}/{content.name})')
    except:
        await message.reply('Something catastrophic happened and I couldn\'t list the files you requested.')
        return

    # join into single chunk
    files = '\n'.join(files)

    # chunk and send as embed object
    for chunk in utility.embedsplit(files, 4096): # max message reply string length is 4096 char
        embed = discord.Embed(
            title = f'{correl} ls:',
            description = chunk,
        )
        await message.reply(embed=embed)

    return





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
    for chunk in utility.embedsplit(files, 4096): # max message reply string length is 4096 char



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
    stringchunks = utility.embedsplit(joinedlines, 4096)
    i = 1
    chunkno = len(list(stringchunks))
    for chunk in utility.embedsplit(joinedlines, 4096): # max message reply string length is 4096 char
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
    stringchunks = utility.embedsplit(joinedlines, 4096)
    i = 1
    chunkno = len(list(stringchunks))
    for chunk in utility.embedsplit(joinedlines, 4096): # max message reply string length is 4096 char
        embed = discord.Embed(
            title = f'cat {kbdata.name} _page {i}/{chunkno}_',
            description = chunk,
        )
        i += 1
        await message.reply(embed=embed)
    return
