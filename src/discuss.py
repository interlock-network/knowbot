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
            discussions(first: 2) {
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

# get discussion titles and urls
discussions = requests.post(url=url, json=json_ls, headers=headers)

# parse returned discussions json
discussions = discussions.json()['data']['repository']['discussions']['nodes']

print(discussions[0]['title'])


