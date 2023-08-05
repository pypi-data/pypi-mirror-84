import base64
import git
import requests
from github import Github
from pprint import pprint
#import argparse

def deleteRepo(owner,repo):
    #parser = argparse.ArgumentParser()
    #parser.add_argument('--owner',help="owner")
    #parser.add_argument('--reponame',help="reponame")
    #args=parser.parse_args()
    #owner=args.owner
    #reponame=args.reponame
    token="b4fa328e0928e75f6db479645b3cad5e8cd740f3" 
    query_url = f"https://api.github.com/repos/{owner}/{repo}" 
    headers = {
      'Authorization': f'token {token}',
      'Accept': 'application/vnd.github.v3+json',
    }
    r = requests.delete(query_url, headers=headers)