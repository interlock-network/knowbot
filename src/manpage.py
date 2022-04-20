##########################################
#
# INTERLOCK KNOWBOT (KNOWLEDGEBASE) DISCORD BOT
# manpage.py
#
##########################################

##########################################
# configure
##########################################

# TO CONFIGURE THIS KNOWBOT,
# REFER TO utility.py

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
CHOOSE A CORRELATIVE LIKE SO
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
    The ls utility displays the names of files in the specified interrogative-correlative.
    The following options are available:

    help    Display overview of specified interrogative-correlative.

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
