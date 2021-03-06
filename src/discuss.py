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
# please REFER to the utility.py configuration section.

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

# define repo command from utility.py
repo = utility.repo

##########################################
# ls discuss
##########################################

async def ls_discuss(message, keyphrase, reply):

    # define title, and discussions list
    title = f'{repo} ls discuss '
    discussions = []
    
    # define query variables
    variables = {
        'owner': utility.organization,
        'reponame': utility.repository,
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
                        number
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
                discussions.append(f'[discuss/{discussion["number"]} ...{discussion["title"]}]({discussion["url"]})')
        else:
            discussions.append(f'[discuss/{discussion["number"]} ...{discussion["title"]}]({discussion["url"]})')

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
                        number
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
            'owner': utility.organization,
            'reponame': utility.repository,
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
                    discussions.append(f'[discuss/{discussion["number"]} ...{discussion["title"]}]({discussion["url"]})')
            else:
                discussions.append(f'[discuss/{discussion["number"]} ...{discussion["title"]}]({discussion["url"]})')

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
    keyphrase = message.content.lower().replace(f'{repo} ls discuss | grep ', '')
    title = f'{repo} ls discuss | grep \'{keyphrase}\''
    discussions = []
    
    # define query variables
    variables = {
        'owner': utility.organization,
        'reponame': utility.repository,
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
            'owner': utility.organization,
            'reponame': utility.repository,
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
        keyphrase = message.content.lower().replace(f'{repo} grep ', '').replace(' discuss', '')
    else:
        keyphrase = message.content.lower().replace(f'{repo} grep ', '').replace(' *', '')
    title = f'{repo} grep \'{keyphrase}\' discuss '

    
    # define query variables
    variables = {
        'owner': utility.organization,
        'reponame': utility.repository,
    }

    # get first 100 (max) discussions
    # ls graphql query
    ls_discussion = """
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
                        number
                    }
                }
            }
        }
    """

    # package final query json for ls command
    json_ls = {
        'query': ls_discussion,
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
                resultlines.append(f'[discuss/{discussion["number"]} ...{discussion["title"]}]({discussion["url"]}): {line}')

    # new ls graphql query with cursor
    ls_discussion = """
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
                        number
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
            'owner': utility.organization,
            'reponame': utility.repository,
            'cursor': querydata['pageInfo']['endCursor']
        } 

        # build new json object
        json_ls = {
            'query': ls_discussion,
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
                    resultlines.append(f'[discuss/{discussion["number"]} ...{discussion["title"]}]({discussion["url"]}): {line}')
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
    keyphrase = message.content.lower().replace(f'{repo} cat discuss/', '')
    title = f'{repo} cat \'discuss/{keyphrase}\' '
    body = []
    lines: list = []

    
    # define query variables
    variables = {
        'owner': utility.organization,
        'reponame': utility.repository,
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
                        number
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
    discussion_title = ''
    discussion_url = ''
    for discussion in querydata['nodes']:
        if str(discussion['number']) == keyphrase:
            body = discussion['body']
            discussion_title = discussion['title']
            discussion_url = discussion['url']

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
                        number
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
            'owner': utility.organization,
            'reponame': utility.repository,
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
            if discussion['number'] == keyphrase:
                body = discussion['body']

        count += 100

    # check for empty search result
    if body == []:
        await message.reply(f'Sorry, but I could not find the discussion you specified.')
        return

    strings = ['_For the full discussion, please click the Title link below._',
            f'**[{discussion_title}]({discussion_url})**', body]
    body = '\n'.join(strings)
    lines = body.splitlines()
    i = 0
    for line in lines:
        lines[i] = utility.cleanup_markdown(line)
        i += 1

    # if called directly by bot.py, reply to message with embed object
    await utility.embed_reply(message, lines, title)
    
    return resultlines
