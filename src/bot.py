##########################################
#
# INTERLOCK KNOWBOT (KNOWLEDGEBASE) DISCORD BOT
# bot.py
#
##########################################

# TODO:
# . mention license in header

##########################################
# configure
##########################################

# TO CONFIGURE THIS KNOWBOT,
# REFER TO utility.py

##########################################
# setup
##########################################

# include local .py files
import manpage
import command
import discuss
import utility

# include others
import os
import discord
from dotenv import load_dotenv

# get repo command from utility.py
repo = utility.repo

# load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_SERVER = os.getenv('DISCORD_SERVER')

# define client
client = discord.Client()

# connect knowbot
@client.event
async def on_ready():
    server = discord.utils.get(client.guilds, name=DISCORD_SERVER)
    print(
        f'{client.user} is connected to server\n'
        f'{server.name}(id: {server.id})'
    )

##########################################
# listen for messages
##########################################

@client.event
async def on_message(message):
    
    # check for cat command to print file
    # manpage help
    if (message.content == f'{repo} cat' or
        message.content == f'{repo} cat ' or
        message.content == f'{repo} cat help'):
        await manpage.cat_help(message)
    # command exec
    elif message.content.startswith(f'{repo} cat discuss/'):
        await discuss.cat_discuss(message)
    elif (message.content.startswith(f'{repo} cat ')):
        await command.cat(message)

    # check for ls command to list directory contents
    # list correlative directories
    if (message.content == f'{repo} ls *'):
        await command.ls_all(message)
    elif (message.content == f'{repo} ls'):
        await command.ls(message)
    elif (message.content == f'{repo} ls '):
        await manpage.ls_list(message)

    # manpage help
    elif (message.content == f'{repo} ls help'):
        await manpage.ls_help(message)
    # display interrogative help
    elif (message.content.startswith(f'{repo} ls help ')):
        await command.ls_help(message)
    # command exec
    elif (message.content == f'{repo} ls discuss'):
        await discuss.ls_discuss(message, '', True)
    elif (message.content.startswith(f'{repo} ls discuss | grep ')):
        await discuss.ls_discuss_grep(message)
    elif (message.content.startswith(f'{repo} ls ') and
        not message.content.__contains__(' | grep ')):
        await command.ls_directory(message)

    # check for ls command to grep directory contents list
    # pipe grep directories ls from specific correlative
    head, delimit, tail = message.content.replace(f'{repo} ls ', '').partition('| grep ')
    if (not head == '' and message.content.__contains__(' | grep ') and
            not message.content.startswith(f'{repo} ls discuss | grep ')):
        await command.ls_correl_grep(message)

    # check for ls command to grep all contents list
    # pipe grep directories ls from specific correlative
    if message.content.startswith(f'{repo} ls | grep '):
        await command.ls_grep(message)

    # check for grep command to grep all contents
    # grep all
    elif (message.content.startswith(f'{repo} grep ') and
        message.content.endswith(' *')):
        await command.grep_all(message)
    elif (message.content.startswith(f'{repo} grep ') and
        message.content.endswith(' discuss')):
        await discuss.grep_discuss(message, '', True)
    try:
        if (message.content.replace(f'{repo} grep ', '').split()[-1] in utility.correl and
                not message.content.startswith(f'{repo} ls')):
            await command.grep_correl(message)
    except IndexError:
        pass

##########################################
# main
##########################################

client.run(DISCORD_TOKEN)
