# INTERLOCK KNOWLEDGEBASE DISCORD BOT

# include local modules
import utility
import command

# include modules
import requests
import json


# setup to query
url = 'https://api.github.com/graphql'
api_token = command.GITHUB_TOKEN
headers = {'Authorization': f'token {api_token}' }

# define query variables
variables = {
    'owner': utility.org,
    'reponame': utility.repo,
}

# ls command for repo discussions

# ls graphql query
ls = """
    query($owner: String!, $reponame: String!) {
        repository(owner: $owner, name: $reponame) {
            discussions(first: 100) {
                totalCount
                nodes {
                    title 
                    url
                }
            }
        }
    }
"""

# package final query json for ls command
json_ls = {
    'query': ls,
    'variables': variables,
}


# ls discussion command
async def ls_discussions(message):

    # define title, and discussions list
    title = f'kb ls discussions '
    discussions = []
    
    # get file contents and return error if no file or directory exists
    try:
        # get discussion titles and urls
        querydata = requests.post(url=url, json=json_ls, headers=headers)
    except:
        await message.reply('I couldn\'t get the discussions you requested from the repository.')
        return

    # parse returned discussions json
    totalcount = querydata.json()['data']['repository']['discussions']['totalCount']
    print(totalcount)
    querydata = querydata.json()['data']['repository']['discussions']['nodes']

    
    for discussion in querydata[:]:
        discussions.append(f'[{discussion["title"]}]({discussion["url"]})')

    # add segment to process >100 discussions here
    # i = 100
    # while i < totalcount:


    # chunk and send as embed object
    await utility.embed_reply(message, discussions, title)

    return


