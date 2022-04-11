# INTERLOCK KNOWLEDGEBASE DISCORD BOT

# include others
import discord

# display ls list for correlative options
async def ls_list(message):
    output = """
CHOOSE A CORRELATIVE LIKE SO
    kb ls how-many
    kb ls how
    kb ls what-kind-of
    kb ls what
    kb ls when
    kb ls where
    kb ls which
    kb ls whither
    kb ls who
    kb ls whose
    kb ls why
    kb ls help
"""
    embed = discord.Embed(
        title = f"KB LS",
        description = output,
    )
    await message.reply(embed=embed)

    return

# display ls help man page
async def ls_help(message):
    output = """
NAME
    kb ls - list directory contents

SYNOPSIS
    kb ls [help] [how-many, how, what-kind-of, what, when, where, which, whither, who, whose, why]

DESCRIPTION
    The ls utility displays the names of files in the specified interrogative-correlative.
    The following options are available:

    help    Display overview of specified interrogative-correlative.

EXAMPLES
    List the contents of the 'what' category:
        kb ls what

    List the contents of the 'why' category:
        kb ls why

    Display a description of the 'how' category:
        kb ls help how
"""
    embed = discord.Embed(
        title = f"KB LS    General Commands Manual",
        description = output,
    )
    await message.reply(embed=embed)
    return

# display cat help man page
async def cat_help(message):
    output = """
NAME
    kb cat - contatenate and print files

SYNOPSIS
    kb cat [help] [file]

DESCRIPTION
    The cat utility reads text or markdown files, writing them to chat. Replies are broken into 2000 character chunks, and this might interfere with markdown formatting, or it might cause a line to be broken in an awkward place. Relative markdown links have been replaced by the absolute url. To prevent previews for all links in chat, the '<' is prepended to each address.

EXAMPLE
    The command:
        kb cat file1.md
    will print the contents of file1.md to chat.
"""
    embed = discord.Embed(
        title = f"KB CAT    General Commands Manual",
        description = output,
    )
    await message.reply(embed=embed)
    return
