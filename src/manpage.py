# INTERLOCK KNOWLEDGEBASE DISCORD BOT

# display help man page
async def cat_help(message):
    output = """
KB-CAT      General Commands Manual

NAME
    kb-cat - contatenate and print files

SYNOPSIS
    kb-cat [--help] [file]

DESCRIPTION
    The cat utility reads text or markdown files, writing them to chat. Replies are broken into 2000 character chunks, and this might interfere with markdown formatting, or it might cause a line to be broken in an awkward place. Relative markdown links have been replaced by the absolute url. To prevent previews for all links in chat, the '<' is prepended to each address.

EXAMPLE
    The command:

        kb-cat file1.md

    will print the contents of file1.md to chat.
"""
    await message.reply(output)
    return
