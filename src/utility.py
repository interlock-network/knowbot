# INTERLOCK KNOWLEDGEBASE DISCORD BOT

# break lond string into chunks
def chunkstring(string, length):
    return (string[i:(length + i)] for i in range(0, len(string), length))

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
