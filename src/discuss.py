##########################################
#
# INTERLOCK KNOWLEDGEBASE DISCORD BOT
# discuss.py
#
##########################################

# TODO
# . include comments in grep discuss
# . create cat for discussion main entry
# .

##########################################
# setup
##########################################

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

##########################################
# ls discuss
##########################################

async def ls_discuss(message, keyphrase, reply):

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
        if (not reply and not keyphrase == ''):
            if discussion['title'].lower().__contains__(keyphrase.lower()):
                discussions.append(f'[discuss/{discussion["title"]}]({discussion["url"]})')
        else:
            discussions.append(f'[discuss/{discussion["title"]}]({discussion["url"]})')

    # new ls graphql query with cursor
    ls = """
        query($owner: String!, $reponame: String!, $cursor: String!) {
            repository(owner: $owner, name: $reponame) {
                discussions(first: 100, after: $cursor) {
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

    # if discussion count >100, resume query at last cursor until reach totalcount
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
            if (not reply and not keyphrase == ''):
                if discussion['title'].lower().__contains__(keyphrase.lower()):
                    discussions.append(f'[discuss/{discussion["title"]}]({discussion["url"]})')
            else:
                discussions.append(f'[discuss/{discussion["title"]}]({discussion["url"]})')

        count += 100

    # check for empty search result
    if (discussions == [] and reply == True):
        await message.reply(f'Sorry, but your search for _{keyphrase}_ did not return any results :/')
        return
    
    # if called directly from bot.py, reply to message with embed object
    if reply:
        # chunk and send as embed object
        await utility.embed_reply(message, discussions, title)

    return discussions

##########################################
# ls discuss | grep
##########################################

async def ls_discuss_grep(message):

    # define title, and discussions list
    keyphrase = message.content.replace('kb ls discuss | grep ', '')
    title = f'kb ls discuss | grep \'{keyphrase}\''
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
        if discussion['title'].lower().__contains__(keyphrase.lower()):
            discussions.append(f'[discuss/{discussion["title"]}]({discussion["url"]})')

    # new ls graphql query with cursor
    ls = """
        query($owner: String!, $reponame: String!, $cursor: String!) {
            repository(owner: $owner, name: $reponame) {
                discussions(first: 100, after: $cursor) {
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

    # if discussion count >100, resume query at last cursor until reach totalcount
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
            if discussion['title'].lower().__contains__(keyphrase.lower()):
                discussions.append(f'[discuss/{discussion["title"]}]({discussion["url"]})')

        count += 100

    # check for empty search result
    if (discussions == [] and reply == True):
        await message.reply(f'Sorry, but your search for _{keyphrase}_ did not return any results :/')
        return
    
    # chunk and send as embed object
    await utility.embed_reply(message, discussions, title)

    return discussions

##########################################
# grep discuss
##########################################

async def grep_discuss(message, keyphrase, reply):

    # get keyphrase, define title, init files list
    resultlines: list = []
    if reply:
        keyphrase = message.content.replace('kb grep ', '').replace(' discuss', '')
    else:
        keyphrase = message.content.replace('kb grep ', '').replace(' *', '')
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

    # new ls graphql query with cursor
    ls = """
        query($owner: String!, $reponame: String!, $cursor: String!) {
            repository(owner: $owner, name: $reponame) {
                discussions(first: 100, after: $cursor) {
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

    # if discussion count >100, resume query at last cursor until reach totalcount
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
            lines = discussion['body'].splitlines()
            for line in lines:
                if line.lower().__contains__(keyphrase.lower()):
                    resultlines.append(f'[discuss/{discussion["title"]}]({discussion["url"]}): {line}')
        count += 100

    # check for empty search result
    if (resultlines == [] and reply == True):
        await message.reply(f'Sorry, but your search for _{keyphrase}_ did not return any results :/')
        return

    # if called directly by bot.py, reply to message with embed object
    if reply:
        await utility.embed_reply(message, resultlines, title)
    
    return resultlines


##########################################
# cat discuss
##########################################

async def cat_discuss(message):

    # get keyphrase, define title, init files list
    resultlines: list = []
    keyphrase = message.content.replace('kb cat discuss/', '')
    title = f'kb cat \'{keyphrase}\''
    body = []

    
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
        print('chirp')
        return

    # parse returned discussions json
    totalcount = querydata.json()['data']['repository']['discussions']['totalCount']
    querydata = querydata.json()['data']['repository']['discussions']
    
    # continue building list discussion title list
    for discussion in querydata['nodes']:
        if discussion['title'].lower() == keyphrase.lower():
            body = discussion['body']

    # new ls graphql query with cursor
    ls = """
        query($owner: String!, $reponame: String!, $cursor: String!) {
            repository(owner: $owner, name: $reponame) {
                discussions(first: 100, after: $cursor) {
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

    # if discussion count >100, resume query at last cursor until reach totalcount
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
            if discussion['title'].lower() == keyphrase.lower():
                body = discussion['body']

        count += 100

    # check for empty search result
    if body == []:
        await message.reply(f'Sorry, but I could not find the discussion you specified.')
        return

    lines = body.splitlines()
    i = 0
    for line in lines:
        lines[i] = utility.cleanup_markdown(line)
        i += 1

    # if called directly by bot.py, reply to message with embed object
    await utility.embed_reply(message, lines, title)
    
    return resultlines
