# INTERLOCK KNOWLEDGEBASE DISCORD BOT

# include local modules
import utility

# include modules
import os
import requests
import json
from dotenv import load_dotenv


# PAT from blairmunroakusa for dev purposes
# scope restricted to only access public repo info
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# setup to query
url = 'https://api.github.com/graphql'
api_token = GITHUB_TOKEN
headers = {'Authorization': f'token {api_token}' }






# ls discussion command
async def ls_discussions(message, keyphrase, reply):

    # define title, and discussions list
    title = f'kb ls discuss '
    discussions = []
    
    # define query variables
    variables = {
        'owner': utility.org,
        'reponame': utility.repo,
    }

    # get first 100 (max) discussions

    # ls graphql query
    ls = """
        query($owner: String!, $reponame: String!) {
            repository(owner: $owner, name: $reponame) {
                discussions(first: 100) {
                    totalCount
                    pageInfo {
                        endCursor
                    }
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

    # get discussion contents and return error if no file or directory exists
    try:
        # get discussion titles and urls
        querydata = requests.post(url=url, json=json_ls, headers=headers)
    except:
        await message.reply('I couldn\'t get the discussions you requested from the repository.')
        return

    # parse returned discussions json
    totalcount = querydata.json()['data']['repository']['discussions']['totalCount']
    querydata = querydata.json()['data']['repository']['discussions']
    
    # continue building list discussion title list
    for discussion in querydata['nodes']:
        if not reply:
            if discussion['title'].lower().__contains__(keyphrase.lower()):
                discussions.append(f'[discuss/{discussion["title"]}]({discussion["url"]})')
        else:
            discussions.append(f'[discuss/{discussion["title"]}]({discussion["url"]})')

    # new ls graphql query with cursor
    ls = """
        query($owner: String!, $reponame: String!, $cursor: String!) {
            repository(owner: $owner, name: $reponame) {
                discussions(first: 10, after: $cursor) {
                    totalCount
                    pageInfo {
                        endCursor
                    }
                    nodes {
                        title 
                        url
                    }
                }
            }
        }
    """

    count = 100
    while count < totalcount:

        # redefine query variables to include cursor to get next page of 100 discussions
        variables = {
            'owner': utility.org,
            'reponame': utility.repo,
            'cursor': querydata['pageInfo']['endCursor']
        } 

        # build new json object
        json_ls = {
            'query': ls,
            'variables': variables,
        }

        # get discussion contents and return error if no file or directory exists
        try:
            # get discussion titles and urls
            querydata = requests.post(url=url, json=json_ls, headers=headers)
        except:
            await message.reply('I couldn\'t get the discussions you requested from the repository.')
            return

        # parse returned discussions json
        querydata = querydata.json()['data']['repository']['discussions']

        # continue building list discussion title list
        for discussion in querydata['nodes']:
            if not reply:
                if discussion['title'].lower().__contains__(keyphrase.lower()):
                    discussions.append(f'[discuss/{discussion["title"]}]({discussion["url"]})')
            else:
                discussions.append(f'[discuss/{discussion["title"]}]({discussion["url"]})')

        count += 100

    if reply:
        # chunk and send as embed object
        await utility.embed_reply(message, discussions, title)

    return discussions


# grep discussion command
async def grep_discussions(message, keyphrase, reply):

    # get keyphrase, define title, init files list
    resultlines: list = []
    keyphrase = message.content.replace('kb grep ', '').replace(' discuss', '')
    title = f'kb grep \'{keyphrase}\' discuss '

    
    # define query variables
    variables = {
        'owner': utility.org,
        'reponame': utility.repo,
    }

    # get first 100 (max) discussions

    # ls graphql query
    ls = """
        query($owner: String!, $reponame: String!) {
            repository(owner: $owner, name: $reponame) {
                discussions(first: 100) {
                    totalCount
                    pageInfo {
                        endCursor
                    }
                    nodes {
                        body
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

    # get discussion contents and return error if no file or directory exists
    try:
        # get discussion titles and urls
        querydata = requests.post(url=url, json=json_ls, headers=headers)
    except:
        await message.reply('I couldn\'t get the discussions you requested from the repository.')
        return

    # parse returned discussions json
    totalcount = querydata.json()['data']['repository']['discussions']['totalCount']
    querydata = querydata.json()['data']['repository']['discussions']
    
    # continue building list discussion title list
    for discussion in querydata['nodes']:
        lines = discussion['body'].splitlines()
        for line in lines:
            if line.lower().__contains__(keyphrase.lower()):
                resultlines.append(f'[discuss/{discussion["title"]}]({discussion["url"]}): {line}')


    await utility.embed_reply(message, resultlines, title)

    return resultlines
"""
    # new ls graphql query with cursor
    ls = 
        query($owner: String!, $reponame: String!, $cursor: String!) {
            repository(owner: $owner, name: $reponame) {
                discussions(first: 10, after: $cursor) {
                    totalCount
                    pageInfo {
                        endCursor
                    }
                    nodes {
                        body
                        title 
                        url
                    }
                }
            }
        }
    

    count = 100
    while count < totalcount:

        # redefine query variables to include cursor to get next page of 100 discussions
        variables = {
            'owner': utility.org,
            'reponame': utility.repo,
            'cursor': querydata['pageInfo']['endCursor']
        } 

        # build new json object
        json_ls = {
            'query': ls,
            'variables': variables,
        }

        # get discussion contents and return error if no file or directory exists
        try:
            # get discussion titles and urls
            querydata = requests.post(url=url, json=json_ls, headers=headers)
        except:
            await message.reply('I couldn\'t get the discussions you requested from the repository.')
            return

        # parse returned discussions json
        querydata = querydata.json()['data']['repository']['discussions']

        # continue building list discussion title list
        for discussion in querydata['nodes']:
            if not reply:
                if discussion['title'].lower().__contains__(keyphrase.lower()):
                    discussions.append(f'[discuss/{discussion["title"]}]({discussion["url"]})')
            else:
                discussions.append(f'[discuss/{discussion["title"]}]({discussion["url"]})')

        count += 100
"""
    #if reply:
        # chunk and send as embed object





"""



# cat discussion command
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
    querydata = querydata.json()['data']['repository']['discussions']['nodes']

    
    for discussion in querydata:
        discussions.append(f'[{discussion["title"]}]({discussion["url"]})')

    # add segment to process >100 discussions here
    # i = 100
    # while i < totalcount:


    # chunk and send as embed object
    await utility.embed_reply(message, discussions, title)

    return
"""

