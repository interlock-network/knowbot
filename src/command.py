##########################################
#
# INTERLOCK KNOWLEDGEBASE DISCORD BOT
# command.py
#
##########################################

# TODO
# . create ls *
# . create grep for each correlative
# . create ls

##########################################
# setup
##########################################

# include local modules
import utility
import discuss

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
kb = g.get_repo(utility.repolong)
repofull = utility.repofull

##########################################
# grep <keyphrase> *
##########################################

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
                    if str(line.lower()).__contains__(keyphrase.lower()):

                        # cleanup line
                        line = utility.cleanup_markdown(line)

                        # condition and add to results
                        resultlines.append(f'[{correl}/{content.name}]({repofull}/blob/master/{correl}/{content.name}): {line}')

    except:
        await message.reply('I couldn\'t get what you requested from the repository.')
        return

    # import discussion line matches and add to result lines list
    # 'False' indicates to grep_discussions that no print is needed
    discussionlines = await discuss.grep_discuss(message, keyphrase, False)
    # 'None' indicates discuss search returned no results; if None, continue
    if not discussionlines == None:
        for discussionline in discussionlines:
            resultlines.append(discussionline)

    # check for empty search result
    if resultlines == []:
        await message.reply(f'Sorry, but your search for _{keyphrase}_ did not return any results :/')
        return

    # chunk and send as embed object
    await utility.embed_reply(message, resultlines, title)

    return

##########################################
# ls | grep <keyphrase>
##########################################

async def ls_grep(message):

    # get keyphrase, define title, init files list
    files: list = []
    keyphrase = message.content.replace('kb ls | grep ', '')
    title = f'kb ls | grep \'{keyphrase}\' '

    # get file contents and return error if no file or directory exists
    try:
        for correl in utility.correl:
            for content in kb.get_contents(correl):
                if content.name.lower().__contains__(keyphrase.lower()):
                    files.append(f'[{correl}/{content.name}]({repofull}/blob/master/{correl}/{content.name})')
    except:
        await message.reply('I couldn\'t get what you requested from the repository.')
        return

    # import discussion lst and add to files list
    # 'False' indicates to grep_discussions that no print is needed
    discussions = await discuss.ls_discuss(message, keyphrase, False)
    # 'None' indicates discuss search returned no results; if None, continue
    if not discussions == None:
        for discussion in discussions:
            files.append(discussion)

    # check for empty search result
    if files == []:
        await message.reply(f'Sorry, but your search for _{keyphrase}_ did not return any results :/')
        return

    # chunk and sed as embed object
    await utility.embed_reply(message, files, title)

    return

##########################################
# ls <correlative> | grep <keyphrase>
##########################################

async def ls_correl_grep(message):

    # get keyphrase, get correlative, define title, init files list
    files: list = []
    correl, delimit, keyphrase = message.content.replace('kb ls ', '').partition(' | grep ')
    title = f'kb ls \'{correl}\' | grep \'{keyphrase}\' '

    # get file contents and return error if no file or directory exists
    try:
        for content in kb.get_contents(correl):
            if content.name.lower().__contains__(keyphrase.lower()):
                files.append(f'[{correl}/{content.name}]({repofull}/blob/master/{correl}/{content.name})')
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

##########################################
# ls
##########################################

async def ls(message):

    # get correlative, define title, init files list
    files: list = []
    title = f'kb ls'
    
    # get file contents and return error if no file or directory exists
    try:
            for content in kb.get_contents(''):
                files.append(f'[{content.name}]({repofull}/{content.name})')
    except:
        await message.reply('I couldn\'t get what you requested from the repository.')
        return

    # append discussions
    files.append(f'[discuss]({repofull}/discussions)')
    
    # chunk and send as embed object
    await utility.embed_reply(message, files, title)

    return

##########################################
# ls *
##########################################

async def ls_all(message):

    # get correlative, define title, init files list
    files: list = []
    title = f'kb ls *'
    
    # get file contents and return error if no file or directory exists
    try:
        for directory in utility.correl:
            for content in kb.get_contents(directory):
                files.append(f'[{directory}/{content.name}]({repofull}/blob/master/{directory}/{content.name})')
    except:
        await message.reply('I couldn\'t get what you requested from the repository.')
        return

    # import discussion lst and add to files list
    # 'False' indicates to grep_discussions that no print is needed
    discussions = await discuss.ls_discuss(message, '', False)
    # 'None' indicates discuss search returned no results; if None, continue
    if not discussions == None:
        for discussion in discussions:
            files.append(discussion)

    # check for empty result
    if files == []:
        await message.reply(f'Sorry, but your attempt to list did not return any results :/')
        return

    # chunk and send as embed object
    await utility.embed_reply(message, files, title)

    return

##########################################
# ls <correlative>
##########################################

async def ls_directory(message):

    # get correlative, define title, init files list
    files: list = []
    correl = message.content.replace('kb ls ', '')
    title = f'kb ls \'{correl}\' '
    
    # get file contents and return error if no file or directory exists
    try:
        for content in kb.get_contents(correl):
            files.append(f'[{correl}/{content.name}]({repofull}/blob/master/{correl}/{content.name})')
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

##########################################
# ls help <correlative>
##########################################

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

##########################################
# cat <filename>
##########################################

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
