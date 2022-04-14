# INTERLOCK KNOWLEDGEBASE DISCORD BOT

# include
import discord

# define repo
repo = 'World-Peace-Labs/testee'
repofull = 'https://github.com/' + repo

# break long string into chunks
def chunkstring(string, length):
   return (string[i:(length + i)] for i in range(0, len(string), length))



# create embed chunks without breaking lines between chunks (to preserve links, etc)
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


# chunk and send as embed object
async def embed_reply(message, content, header):

    #join lines of content
    content = '\n'.join(content)
    
    # chunk and send as embed object
    i = 1
    chunkno = len(list(embedsplit(content, 4096)))
    for chunk in embedsplit(content, 4096): # max message reply string length is 4096 char
        embed = discord.Embed(
            title = f'{header} _page {i}/{chunkno}_',
            description = chunk,
        )
        await message.reply(embed=embed)
        i += 1



# convert regular markdown into crappy discord markdown
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


# list of correlatives
correl = ['how-many',
        'how',
        'what-kind-of',
        'what',
        'when',
        'where',
        'which',
        'whither',
        'who',
        'whose',
        'why']
