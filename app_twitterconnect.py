#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 03 21:05:00 2021
@author: iv
"""
import sys
import os
import requests as rq
import pandas as pd
import json
import glob
from flask import Flask, jsonify
import logging
import yaml
import tweepy

with open("config.yaml", "r") as stream:
    auth_tweeter = yaml.safe_load(stream)
    stream.close()

api_key = auth_tweeter['api_key']
api_key_secret = auth_tweeter['api_key_secret']
acces_token = auth_tweeter['acces_token']
acces_token_secret = auth_tweeter['acces_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(acces_token, acces_token_secret)
api = tweepy.API(auth)
# for tweet in tweepy.Cursor(api.search_tweets, q='tweepy').items(10):
#     print(tweet.text)

api.update_status("Hello world!! this is a new incredible account to post updates about my trading bot results!!!")

# 'curl --request GET 'https://api.twitter.com/2/tweets/search/recent?query=from:twitterdev' --header
# 'Authorization: Bearer $BEARER_TOKEN'