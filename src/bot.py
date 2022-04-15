# INTERLOCK KNOWLEDGEBASE DISCORD BOT

# TODO:
# . mention license in header
# x get simple hello world running
# x implement internals to interact with discord chat
# x implement internals to interact with github API
# x implement cat functionality
# . implement ls functionality

# include local .py files
import manpage
import command
import discuss

# include others
import os
import discord
from dotenv import load_dotenv

# load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_SERVER = os.getenv('DISCORD_SERVER')

# define client
client = discord.Client()

# connect kb-bot
@client.event
async def on_ready():
    server = discord.utils.get(client.guilds, name=DISCORD_SERVER)
    print(
        f'{client.user} is connected to server\n'
        f'{server.name}(id: {server.id})'
    )

# listen for messages
@client.event
async def on_message(message):
    
    # check for cat command to print file
    # manpage help
    if (message.content == 'kb cat' or
        message.content == 'kb cat ' or
        message.content == 'kb cat --help'):
        await manpage.cat_help(message)
    # command exec
    elif (message.content.startswith('kb cat ')):
        await command.cat(message)

    # check for ls command to list directory contents
    # list correlative directories
    if (message.content == 'kb ls' or
        message.content == 'kb ls '):
        await manpage.ls_list(message)
    # manpage help
    elif (message.content == 'kb ls help'):
        await manpage.ls_help(message)
    # display interrogative help
    elif (message.content.startswith('kb ls help ')):
        await command.ls_help(message)
    # command exec
    elif (message.content == 'kb ls discuss'):
        await discuss.ls_discussions(message, '', True)
    elif (message.content.startswith('kb ls ') and
        not message.content.__contains__(' | grep ')):
        await command.ls(message)

    # check for ls command to grep directory contents list
    # pipe grep directories ls from specific correlative
    head, delimit, tail = message.content.replace('kb ls ', '').partition('| grep ')
    if (not head == '' and message.content.__contains__(' | grep ')):
        await command.ls_correl_grep(message)

    # check for ls command to grep all contents list
    # pipe grep directories ls from specific correlative
    if message.content.startswith('kb ls | grep '):
        await command.ls_grep(message)

    # check for grep command to grep all contents
    # grep all
    elif (message.content.startswith('kb grep ') and
        message.content.endswith(' *')):
        await command.grep_all(message)


# main
client.run(DISCORD_TOKEN)
