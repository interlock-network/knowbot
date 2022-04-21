# This is free-as-in-freedom software,
# protected by the GNU General Public License v3.0
##########################################
#
# INTERLOCK KNOWBOT (KNOWLEDGEBASE) DISCORD BOT
# manpage.py
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

# include others
import discord
import utility

# define repo command from utility.py
repo = utility.repo

##########################################
# ls list options
##########################################

async def ls_list(message):
    output = f"""
CHOOSE A DIRECTORY LIKE SO
    {repo} ls how-many
    {repo} ls how
    {repo} ls what-kind-of
    {repo} ls what
    {repo} ls when
    {repo} ls where
    {repo} ls which
    {repo} ls whither
    {repo} ls who
    {repo} ls whose
    {repo} ls why
    {repo} ls help
"""
    embed = discord.Embed(
        title = f"{repo.upper()} LS",
        description = output,
    )
    await message.reply(embed=embed)

    return

##########################################
# ls help
##########################################

async def ls_help(message):
    output = f"""
NAME
    {repo} ls - list directory contents

SYNOPSIS
    {repo} ls [help] [how-many, how, what-kind-of, what, when, where, which, whither, who, whose, why]

DESCRIPTION
    The ls utility displays the names of files in the specified directory.
    The following options are available:

    help    Display README of specified directory.

EXAMPLES
    List the contents of the 'what' category:
        {repo} ls what

    List the contents of the 'why' category:
        {repo} ls why

    Display a description of the 'how' category:
        {repo} ls help how
"""
    embed = discord.Embed(
        title = f"{repo.upper()} LS    General Commands Manual",
        description = output,
    )
    await message.reply(embed=embed)
    return

##########################################
# display cat help man page
##########################################

async def cat_help(message):
    output = f"""
NAME
    {repo} cat - contatenate and print files

SYNOPSIS
    {repo} cat [help] [file]

DESCRIPTION
    The cat utility reads text or markdown files, writing them to chat. Replies are broken into 2000 character chunks, and this might interfere with markdown formatting, or it might cause a line to be broken in an awkward place. Relative markdown links have been replaced by the absolute url. To prevent previews for all links in chat, the '<' is prepended to each address.

EXAMPLE
    The command:
        {repo} cat file1.md
    will print the contents of file1.md to chat.
"""
    embed = discord.Embed(
        title = f"{repo.upper()} CAT    General Commands Manual",
        description = output,
    )
    await message.reply(embed=embed)
    return

##########################################
# display main help page
##########################################

async def help(message):

    output = f"""
Knowbot is a Discord bot that connects to a github knowledgebase repository, and emulates a _Linux bash terminal_ in a Discord channel, or direct message with Knowbot itself.

This particular knowbot is connected to the **{utility.repository}** repository, owned by **{utility.organization}**.

To use knowbot on this directory '**{repo}**' is the command that indicates to knowbot you would like to interact with **{utility.repository}**.

**Please type the following commands to learn how to use Knowbot:**

knowbot commands
knowbot examples

Or visit the [README here](https://github.com/interlock-network/knowbot/README.md)

"""


    embed = discord.Embed(
        title = f"HOW TO USE KNOWBOT FOR {utility.repository.upper()} REPOSITORY.",
        description = output,
    )
    await message.reply(embed=embed)
    return

##########################################
# display commands menu
##########################################

async def menu(message):

    output = f"""
This knowbot is configured to work with the **{utility.repository}** reposistory.

Commands:

list all directories in home
**{repo} ls**
list all contents of all directories in home
**{repo} ls ***
list all contents in specified directory
**{repo} ls <directory>**
search for <searchphrase> in all contents
**{repo} grep <searchphrase> ***
search of searchphrase in specified directory
**{repo} grep <searchphrase> <directory>**
print file contents
**{repo} cat <directory>/<filename>**
pipe list all directory contents to search for searchphrase
**{repo} ls * | grep <searchphrase>**
pipe list contents of specific directory to search for searchphrase
**{repo} ls <directory> | grep <searchphrase>**

"""


    embed = discord.Embed(
        title = f"MENU OF KNOWBOT COMMANDS",
        description = output,
    )
    await message.reply(embed=embed)
    return
