import base64
import git
import requests
from github import Github
from pprint import pprint
#import argparse

def createRepo(reponame):
   # parser = argparse.ArgumentParser()
   # parser.add_argument('--reponame',help="reponame")
   # args=parser.parse_args()
   # reponame=args.reponame
    g = Github("2e3f647b342094bd5d24839870de1eed15126af2") 
    u=g.get_user()
    repo = u.create_repo(reponame)
    pprint("your repositiory created successfully")
 