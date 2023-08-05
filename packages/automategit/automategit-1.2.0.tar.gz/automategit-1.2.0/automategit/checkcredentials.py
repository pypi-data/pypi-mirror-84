import base64
import git
import requests
from github import Github
from pprint import pprint
#import argparse

def checkCredentials(user,password):
  #parser = argparse.ArgumentParser()
  #parser.add_argument('--username',help="username")
  #parser.add_argument('--password',help="password")
  #args=parser.parse_args()
  #user=args.username
  #password=args.password
  g=Github()
  username = g.get_user(user)
  pprint("Authentication successful!!")
  pprint("Your Repositories are:")
  for repo in username.get_repos():
        pprint(repo.name)