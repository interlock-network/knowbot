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
kb = g.get_repo(utility.repo)
repofull = utility.repofull

# grep all command
async def grep_all(message):

    # get keyphrase, define title, init files list
    resultlines: list = []
    keyphrase = message.content.replace('kb grep ', '').replace(' *', '')
    title = f'kb grep \'{keyphrase}\' '

    # get file contents and return error if no file or directory exists
    try:
        for correl in utility.correl:
            for content in kb.get_contents(correl):

                # get decoded lines
                lines = content.decoded_content.splitlines()

                for line in lines:
                    if str(line).__contains__(keyphrase):

                        # cleanup line
                        line = utility.cleanup_markdown(line)

                        # condition and add to results
                        resultlines.append(f'[{correl}/{content.name}]({repofull}/blob/master/{correl}/{content.name}): {line}')

    except:
        await message.reply('I couldn\'t get what you requested from the repository.')
        return

    # check for empty search result
    if resultlines == []:
        await message.reply(f'Sorry, but your search for _{keyphrase}_ did not return any results :/')
        return

    # chunk and send as embed object
    await utility.embed_reply(message, resultlines, title)

    return

# pipe ls all to grep command
async def ls_grep(message):

    # get keyphrase, define title, init files list
    files: list = []
    keyphrase = message.content.replace('kb ls | grep ', '')
    title = f'kb ls | grep \'{keyphrase}\' '

    # get file contents and return error if no file or directory exists
    try:
        for correl in utility.correl:
            for content in kb.get_contents(correl):
                if content.name.__contains__(keyphrase):
                    files.append(f'[{content.name}]({repofull}/blob/master/{correl}/{content.name})')
    except:
        await message.reply('I couldn\'t get what you requested from the repository.')
        return

    # check for empty search result
    if files == []:
        await message.reply(f'Sorry, but your search for _{keyphrase}_ did not return any results :/')
        return

    # chunk and send as embed object
    await utility.embed_reply(message, files, title)

    return

# pipe ls correlative to grep command
async def ls_correl_grep(message):

    # get keyphrase, get correlative, define title, init files list
    files: list = []
    correl, delimit, keyphrase = message.content.replace('kb ls ', '').partition(' | grep ')
    title = f'kb ls \'{correl}\' | grep \'{keyphrase}\' '

    # get file contents and return error if no file or directory exists
    try:
        for content in kb.get_contents(correl):
            if content.name.__contains__(keyphrase):
                files.append(f'[{content.name}]({repofull}/blob/master/{correl}/{content.name})')
    except:
        await message.reply('I couldn\'t get what you requested from the repository.')
        return

    # check for empty search result
    if files == []:
        await message.reply(f'Sorry, but your search for _{keyphrase}_ did not return any results :/')
        return

    # chunk and send as embed object
    await utility.embed_reply(message, files, title)

    return

# ls command
async def ls(message):

    # get correlative, define title, init files list
    files: list = []
    correl = message.content.replace('kb ls ', '')
    title = f'kb ls \'{correl}\' '
    
    # get file contents and return error if no file or directory exists
    try:
        for content in kb.get_contents(correl):
            files.append(f'[{content.name}]({repofull}/blob/master/{correl}/{content.name})')
    except:
        await message.reply('I couldn\'t get what you requested from the repository.')
        return

    # check for empty search result
    if files == []:
        await message.reply(f'Sorry, but your search for _{keyphrase}_ did not return any results :/')
        return

    # chunk and send as embed object
    await utility.embed_reply(message, files, title)

    return

# ls command switch help
async def ls_help(message):

    # define title and get filename
    correl = message.content.strip('kb ls help ')
    title = f'kb ls help \'{correl}\' '

    # get file contents and return error if no file or directory exists
    try:
        kbdata = kb.get_contents(correl + '/README.md')
    except:
        await message.reply('I couldn\'t get what you requested from the repository, or the correlative doesn\'t exist.')
        return

    # decode file contents and return error if input is actually directory
    content = kbdata.decoded_content

    # put into form that will display lines properly
    lines = content.splitlines()

    # cleanup lines
    i = 0
    for line in lines:
        lines[i] = utility.cleanup_markdown(line)
        i += 1 

    # chunk and send as embed object
    await utility.embed_reply(message, lines, title)

    return

# bash-style cat command
async def cat(message):

    # define title and get filename
    filename = message.content.strip('kb cat ')
    title = f'kb cat \'{filename}\' '

    # get file contents and return error if no file or directory exists
    try:
        kbdata = kb.get_contents(filename)
    except:
        await message.reply('I couldn\'t get what you requested from the repository, or the file doesn\'t exist.')
        return

    # decode file contents and return error if input is actually directory
    try:
        content = kbdata.decoded_content
    except:
        await message.reply(f'\'{filename}\' is actually a directory, nothing to print.')
        return

    # get decoded lines
    lines = content.splitlines()

    # cleanup lines
    i = 0
    for line in lines:
        lines[i] = utility.cleanup_markdown(line)
        i += 1 

    # chunk and send as embed object
    await utility.embed_reply(message, lines, title)

    return
