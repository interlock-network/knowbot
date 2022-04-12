# INTERLOCK KNOWLEDGEBASE DISCORD BOT

# break long string into chunks
def chunkstring(string, length):
   return (string[i:(length + i)] for i in range(0, len(string), length))



# create embed chunks without breaking lines between chunks (to preserve links, etc)
def embedsplit(string, length):

    # cycle through string breaking into nice chunks
    out: list = []
    while True:
        
        # create chunk list from generator
        inter = list(chunkstring(string, 4096))
        
        # split first chunk into lines
        intersplit = inter[0].split('\n')
    
        # trim off interrupted last line
        tail = intersplit.pop()
        
        # add trimmed chunk to output variable after rejoining lines
        out.append('\n'.join(intersplit))

        # if there are more chunks to process, throw out chunk just processed
        if len(inter) > 1:
            inter = inter[1:]
        else:
            break

        # before processing next chunk, add trimmed tail to beginning of chunk
        string = tail + ''.join(inter)
        
    return out

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
