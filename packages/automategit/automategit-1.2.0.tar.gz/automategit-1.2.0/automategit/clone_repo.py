import base64
import git
import requests
#import argparse

def cloneRepo(url,path):
    #parser = argparse.ArgumentParser()
    #parser.add_argument('--url',help="enter your url")
    #parser.add_argument('--path',help="enter path where you want to store")
    #args=parser.parse_args()
    url=args.url
    path=args.path
    git.Repo.clone_from(url,to_path=path)