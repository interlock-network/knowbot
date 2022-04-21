# This is free-as-in-freedom software,
# protected by the GNU General Public License v3.0
##########################################
#
# INTERLOCK KNOWBOT (KNOWLEDGEBASE) DISCORD BOT
# command.py
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

# include local modules
import utility
import discuss

# include others
import os
import discord
import requests
from dotenv import load_dotenv
from github import Github

# personal access token generated for repository by user or org owner
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
g = Github(GITHUB_TOKEN)

# define and get repo
repository = g.get_repo(utility.repolong)
repofull = utility.repofull

# define repo command from utility.py
repo = utility.repo

##########################################
# grep <keyphrase> *
##########################################

async def grep_all(message):

    # get keyphrase, define title, init files list
    resultlines: list = []
    keyphrase = message.content.replace(f'{repo} grep ', '').replace(' *', '')
    title = f'{repo} grep \'{keyphrase}\' '

    # get file contents and return error if no file or directory exists
    try:
        for directory in utility.directories:
            for content in repository.get_contents(directory):

                # get decoded lines
                lines = content.decoded_content.splitlines()

                for line in lines:
                    if str(line.lower()).__contains__(keyphrase.lower()):

                        # cleanup line
                        line = utility.cleanup_markdown(line)

                        # condition and add to results
                        resultlines.append(f'[{directory}/{content.name}]({repofull}/blob/master/{directory}/{content.name}): {line}')

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
# grep <keyphrase> <directory>
##########################################

async def grep_directory(message):

    # get keyphrase, define title, init files list
    resultlines: list = []
    keyphrase = message.content.replace(f'{repo} grep ', '').replace(message.content.split()[-1], '').strip()
    directory = message.content.split()[-1]
    title = f'{repo} grep \'{keyphrase}\' \'{directory}\''

    # reject empty search term
    if keyphrase == '':
        await message.reply(f'A blank search term will return way too many results. You need to actually search for something.')
        return

    # get file contents and return error if no file or directory exists
    try:
        for content in repository.get_contents(directory):

            # get decoded lines
            lines = content.decoded_content.splitlines()

            for line in lines:
                if str(line.lower()).__contains__(keyphrase.lower()):

                    # cleanup line
                    line = utility.cleanup_markdown(line)

                    # condition and add to results
                    resultlines.append(f'[{directory}/{content.name}]({repofull}/blob/master/{directory}/{content.name}): {line}')

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

##########################################
# ls | grep <keyphrase>
##########################################

async def ls_grep(message):

    # get keyphrase, define title, init files list
    files: list = []
    keyphrase = message.content.replace(f'{repo} ls * | grep ', '')
    title = f'{repo} ls * | grep \'{keyphrase}\' '

    # get file contents and return error if no file or directory exists
    try:
        for directory in utility.directories:
            for content in repository.get_contents(directory):
                if content.name.lower().__contains__(keyphrase.lower()):
                    files.append(f'[{directory}/{content.name}]({repofull}/blob/master/{directory}/{content.name})')
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
# ls <directory> | grep <keyphrase>
##########################################

async def ls_directory_grep(message):

    # get keyphrase, get directory, define title, init files list
    files: list = []
    directory, delimit, keyphrase = message.content.replace(f'{repo} ls ', '').partition(' | grep ')
    title = f'{repo} ls \'{directory}\' | grep \'{keyphrase}\' '

    # get file contents and return error if no file or directory exists
    try:
        for content in repository.get_contents(directory):
            if content.name.lower().__contains__(keyphrase.lower()):
                files.append(f'[{directory}/{content.name}]({repofull}/blob/master/{directory}/{content.name})')
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

    # define title, init files list
    files: list = []
    title = f'{repo} ls'
    
    # get file contents and return error if no file or directory exists
    try:
            for content in repository.get_contents(''):
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

    # define title, init files list
    files: list = []
    title = f'{repo} ls *'
    
    # get file contents and return error if no file or directory exists
    try:
        for directory in utility.directories:
            for content in repository.get_contents(directory):
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
# ls <directory>
##########################################

async def ls_directory(message):

    # get directory, define title, init files list
    files: list = []
    directory = message.content.replace(f'{repo} ls ', '')
    title = f'{repo} ls \'{directory}\' '
    
    # get file contents and return error if no file or directory exists
    try:
        for content in repository.get_contents(directory):
            files.append(f'[{directory}/{content.name}]({repofull}/blob/master/{directory}/{content.name})')
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
# ls help <directory>
##########################################

async def ls_help(message):

    # define title and get filename
    directory = message.content.strip(f'{repo} ls help ')
    title = f'{repo} ls help \'{directory}\' '

    # get file contents and return error if no file or directory exists
    try:
        repodata = repository.get_contents(directory + '/README.md')
    except:
        await message.reply('I couldn\'t get what you requested from the repository, or the directory doesn\'t exist.')
        return

    # dec de file contents and return error if input is actually directory
    content = repodata.decoded_content

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
    filename = message.content.strip(f'{repo} cat ')
    title = f'{repo} cat \'{filename}\' '

    # get file contents and return error if no file or directory exists
    try:
        repodata = repository.get_contents(filename)
    except:
        await message.reply('I couldn\'t get what you requested from the repository, or the file doesn\'t exist.')
        return

    # decode file contents and return error if input is actually directory
    try:
        content = repodata.decoded_content
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
