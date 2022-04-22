# This is free-as-in-freedom software,
# protected by the GNU General Public License v3.0
# license copyright (C) of the Free Software Foundation
##########################################
#
# INTERLOCK KNOWBOT (KNOWLEDGEBASE) DISCORD BOT
# bot.py
#
##########################################
# contributors:
# blairmunroakusa
#

##########################################
# configure
##########################################

# To configure this Knowbot,
# please REFER to the utility.py configuration section.

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
    
    # check for general help command
    if (message.content == f'{repo}' or
        message.content == f'{repo} ' or
        message.content.lower() == 'knowbot' or
        message.content.lower() == 'knowbot ' or
        message.content.lower() == 'knowbot help'):
        await manpage.help(message)

    # check for command menu command
    elif (message.content == f'{repo} help' or
        message.content == f'{repo} commands' or
        message.content == f'{repo} command' or
        message.content == f'knowbot commands' or
        message.content == f'knowbot command'):
        await manpage.menu(message)

    # check for examples command
    elif (message.content == f'{repo} examples' or
        message.content == f'{repo} example' or
        message.content == f'knowbot examples' or
        message.content == f'knowbot example'):
        await manpage.example(message)
    # check for cat command to print file
    # manpage help
    elif (message.content == f'{repo} cat' or
        message.content == f'{repo} cat ' or
        message.content == f'{repo} cat help'):
        await manpage.cat_help(message)

    # print discussion number xx
    elif message.content.startswith(f'{repo} cat discuss/'):
        await discuss.cat_discuss(message)

    # print file at directory/filename
    elif (message.content.startswith(f'{repo} cat ')):
        await command.cat(message)

    # check for ls command to list directory contents
    # list all contents in knowledgebase
    elif (message.content == f'{repo} ls *'):
        await command.ls_all(message)

    # list all directories and contents in repo home
    elif (message.content == f'{repo} ls'):
        await command.ls(message)

    # manpage help
    elif (message.content == f'{repo} ls help'):
        await manpage.ls_help(message)

    # display interrogative help
    elif (message.content.startswith(f'{repo} ls help ')):
        await command.ls_help(message)

    # list all discussions
    elif (message.content == f'{repo} ls discuss'):
        await discuss.ls_discuss(message, '', True)

    # search through list of discussion titles
    elif (message.content.startswith(f'{repo} ls discuss | grep ')):
        await discuss.ls_discuss_grep(message)

    # list all files in particular directory
    elif (message.content.startswith(f'{repo} ls ') and
        not message.content.__contains__(' * | grep ') and
        not message.content.__contains__(' | grep ')):
        await command.ls_directory(message)

    # check for ls command to grep directory contents list
    # pipe grep directories ls from specific directory
    head, delimit, tail = message.content.replace(f'{repo} ls ', '').partition('| grep ')
    if (not head == '* ' and message.content.__contains__(' | grep ') and
        not message.content.startswith(f'{repo} ls discuss | grep ')):
        await command.ls_directory_grep(message)

    # check for ls command to grep all contents list
    # pipe grep directories ls from specific directory
    if message.content.startswith(f'{repo} ls * | grep '):
        await command.ls_grep(message)

    # check for grep command to grep all contents
    # grep all
    elif (message.content.startswith(f'{repo} grep ') and
        message.content.endswith(' *')):
        await command.grep_all(message)

    # search through all discussions
    elif (message.content.startswith(f'{repo} grep ') and
        message.content.endswith(' discuss')):
        await discuss.grep_discuss(message, '', True)

    # search through all contents of particular directory
    try:
        if (message.content.replace(f'{repo} grep ', '').split()[-1] in utility.directories and
                not message.content.startswith(f'{repo} ls')):
            await command.grep_directory(message)
    except IndexError:
        pass

##########################################
# main
##########################################

client.run(DISCORD_TOKEN)
