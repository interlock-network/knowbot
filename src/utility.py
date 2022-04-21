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
# change the three variables below, and make the
# list match your repository's directories

# define repository and organization
organization = 'interlock-network' # OR USER
repository = 'interlock-kb'

# define repository command
#
# for example, for repository called
# 'knowledgebase', use 'kb'
repo = 'kb'

# list of directories in repository
directories = [
        'how-many',
        'how',
        'what-kind-of',
        'what',
        'when',
        'where',
        'which',
        'whither',
        'who',
        'whose',
        'why',
        ]

##########################################
# setup
#########################################

# form repository URL strings
repolong = organization + '/' + repository
repofull = 'https://github.com/' + repolong

## include
import discord

##########################################
# break long string into chunks
##########################################

def chunkstring(string, length):
   return (string[i:(length + i)] for i in range(0, len(string), length))


##########################################
# create embed chunks, preserving links and format
##########################################

def embedsplit(string, length):

    # cycle through string breaking into nice chunks
    out: list = []
    ticks = 0
    while True:
        
        # create chunk list from generator
        inter = list(chunkstring(string, 4096))

        # split first chunk into lines
        theselines = inter[0].split('\n')
    
        # trim off interrupted last line
        if len(string) > 4096:
            tail = theselines.pop()

        # count number of triple ticks in chunk
        for line in theselines:
            if line[0:3] == '```':             
                ticks += 1

        # TODO MAKE BLOCK CONTINUATION WORK NON-SHITTY
        # if odd number, then the a code block has been broken by the chunk
        # ... prepend ticks to end and beginning of current and next chunk
        if ticks % 2 == 1:
            if len(inter) > 1:
                tail = '```\n' + tail
            ticks += 1
                
        # add trimmed chunk to output variable after rejoining lines
        out.append('\n'.join(theselines))

        # if there are more chunks to process, throw out chunk just processed
        if len(inter) > 1:
            inter = inter[1:]
        else:
            break

        # before processing next chunk, add trimmed tail to beginning of chunk
        string = tail + ''.join(inter)
        
        
    return out

##########################################
# chunk and send as embed object
##########################################

async def embed_reply(message, content, header):

    #join lines of conten
    content = '\n'.join(content)
    
    # chunk and send as embed object
    i = 1
    chunkno = len(list(embedsplit(content, 4096)))
    for chunk in embedsplit(content, 4096): # max message reply string length is 4096 char
        #print(chunk)
        embed = discord.Embed(
            title = f'{header} _page {i}/{chunkno}_',
            description = chunk,
        )
        await message.reply(embed=embed)
        i += 1

##########################################
# convert regular markdown into discord markdown
##########################################

def cleanup_markdown(line):

    # strip off artifacts
    line = str(line).strip('b\'"!')

    # deal with nonexistant discord markdown headers
    if str(line).startswith('##### '):
        line = line.replace('##### ', '_') + '_'
    if str(line).startswith('#### '):
        line = line.replace('#### ', '__') + '__'
    if str(line).startswith('### '):
        line = line.replace('### ', '***') + '***'
    if str(line).startswith('## '):
        line = line.replace('## ', '**') + '**'
    if str(line).startswith('# '):
        line = line.replace('# ', '__**') + '**__'

    line = line.replace(']( ', '](' + repofull + '/blob/master/')

    # expand relative links into absolute links
    line = line.replace('](.', '](' + repofull + '/blob/master')


    return line


