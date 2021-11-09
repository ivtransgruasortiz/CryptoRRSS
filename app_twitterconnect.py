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
import numpy as np
import json
import glob
from flask import Flask, jsonify
import logging
import yaml
import tweepy
from textblob import TextBlob
import re
# Importing the NaiveBayesAnalyzer classifier from NLTK
from textblob.sentiments import NaiveBayesAnalyzer
from googletrans import Translator

with open("config.yaml", "r") as stream:
    auth_tweeter = yaml.safe_load(stream)
    stream.close()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

api_key = auth_tweeter['api_key']
api_key_secret = auth_tweeter['api_key_secret']
acces_token = auth_tweeter['acces_token']
acces_token_secret = auth_tweeter['acces_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(acces_token, acces_token_secret)
api = tweepy.API(auth)


def get_name(x):
    result = x['screen_name']
    return result


def sent_analisys(x):
    blob_object = TextBlob(x, analyzer=NaiveBayesAnalyzer())
    analysis = blob_object.sentiment
    # return [str(x) for x in analysis]
    analysis = '-'.join([str(x) for x in analysis])
    return analysis


def filtertext(x, excel_file):
    path = os.getcwd()
    df_palabras = pd.read_excel(path + '/' + excel_file)
    df_palabras = df_palabras.fillna(0)
    lista_words = list(df_palabras['PALABRAS'].values) + \
                  list(df_palabras['hastag'].values) + \
                  list(df_palabras['arroba'].values)
    # lista_words = list(filter((0).__ne__, lista_words))
    lista_words = [x for x in lista_words if x != 0]
    result = []
    for word in lista_words:
        tag = bool(re.search(word, x.lower()))
        result.append(tag)
    return max(result)


def translate_en(x, dest='en'):
    translator = Translator()
    result = translator.translate(x, dest='en').text
    return result


userid_list = ('CriptoNoticias', 'bit2me', 'MundoCrypto_ES', 'Tesla',
               'cryptocom', 'elonmusk', 'nayibbukele', 'Cointelegraph', 'crypto', 'CoinMarketCap',
               'ForbesCrypto', 'CryptoBoomNews', 'BTCTN', 'solana', 'CoinbasePro', 'coingecko', 'CoinDesk',
               'blockchain', 'healthy_pockets', 'wallstwolverine'
               )

userid_list = ('CriptoNoticias', 'coingecko', 'CoinDesk', 'blockchain', 'MundoCrypto_ES', 'bit2me', 'healthy_pockets',
               'wallstwolverine'
               )


def json_sentiment(userid_list=userid_list, count_twits=3):
    twits_df = pd.DataFrame()
    for userid in userid_list:
        tweets = api.user_timeline(screen_name=userid,
                                   # 200 is the maximum allowed count
                                   count=count_twits,
                                   include_rts=False,
                                   # Necessary to keep full_text
                                   # otherwise only the first 140 words are extracted
                                   tweet_mode='extended'
                                   )
        tweets_1 = [x._json for x in tweets]
        twits_df_1 = pd.DataFrame(tweets_1)
        twits_df = pd.concat([twits_df, twits_df_1])
    twits_df['has_keys'] = np.vectorize(filtertext)(twits_df['full_text'], 'Palabras_Crypto.xlsx')
    twits_df = twits_df[twits_df['has_keys'] == True]
    twits_df_en = twits_df[twits_df['lang'] == 'en'].reset_index()
    twits_df_others = twits_df[twits_df['lang'] != 'en'].reset_index()
    twits_df_others['full_text'] = np.vectorize(translate_en)(twits_df_others['full_text'])
    twits_df = pd.concat([twits_df_en, twits_df_others])
    twits_df['username'] = np.vectorize(get_name)(twits_df['user'])
    twits_df = twits_df.reset_index()
    twits_df['result'] = np.vectorize(sent_analisys)(twits_df['full_text'])
    twits_df['result2'] = twits_df['result'].str.split('-')
    twits_df['sent_analisys_result'] = np.vectorize(lambda x: x[0])(twits_df['result2'])
    twits_df['sent_analisys_pos'] = np.vectorize(lambda x: float(x[1]))(twits_df['result2'])
    twits_df['sent_analisys_neg'] = np.vectorize(lambda x: float(x[2]))(twits_df['result2'])
    twits_df = twits_df[['id', 'full_text', 'lang', 'has_keys', 'username', 'sent_analisys_result', 'sent_analisys_pos',
                         'sent_analisys_neg']]
    media_pos = twits_df['sent_analisys_pos'].mean()
    media_neg = twits_df['sent_analisys_neg'].mean()
    media_str = 'pos' if media_pos > media_neg else 'neg'
    result = {'prob_positive': media_pos,
              'prob_negative': media_neg,
              'prob_conclusion': media_str}
    return result


# a = json_sentiment(count_twits=2)

#
# ##### Traductor
# text = 'Hola'
# from googletrans import Translator
# translator = Translator()
# translator.translate(text, dest='en').text
# translator.translate(text).text
#
# from textblob import TextBlob
# blob = TextBlob('comment ca va ?')
# blob.translate(to='en')
#
#
# from translate import Translator
# translator = Translator(to_lang="zh")
# translation = translator.translate("This is a pen.")
#
# ##############################################



# # Applying the NaiveBayesAnalyzer
# blob_object = TextBlob(tweet.text, analyzer=NaiveBayesAnalyzer())
# # Running sentiment analysis
# analysis = blob_object.sentiment
# print(analysis)


# api.available_trends()
# api.search_tweets("crypto")


# # Get n-messages
# for tweet in tweepy.Cursor(api.search_tweets, q='tweepy').items(10):
#     print(tweet.text)

# # Writting direct message
# api.update_status("Hello world!! this is a new incredible account to post updates about my trading bot results!!!")

# # Requests curl
# 'curl --request GET 'https://api.twitter.com/2/tweets/search/recent?query=from:twitterdev' --header
# 'Authorization: Bearer $BEARER_TOKEN'


# corpus_tweets = api.search_tweets('mana', count=200)
# for tweet in corpus_tweets:
#     print(tweet.text)

# for status in tweepy.Cursor(api.search_tweets, "crypto",
#                             count=100).items(250):
#     print(status.text)

### twits from account

# userid_list_all = ["CriptoNoticias", "bit2me", 'litecoin', 'polkadot_es', 'MundoCrypto_ES', 'CoinbaseSupport', 'USATODAY',
#                'BBCNews', 'nytimes', 'economics', 'markets', 'FT', 'Citi', 'GoldmanSachs', 'business', 'Tesla',
#                'jpmorgan', 'BusinessInsider', 'SergeyNazarov', 'chainlink', 'cryptocom', 'binance',
#                'cardano_updates', 'BBCBreaking', 'TheEconomics', 'elonmusk', 'FinancialTimes', 'avalancheavax',
#                'nayibbukele', 'Cointelegraph', 'crypto', 'CoinMarketCap', 'ForbesCrypto', 'CryptoBoomNews', 'BTCTN',
#                'solana', 'CoinbasePro', 'coingecko', 'CoinDesk', 'blockchain'
#                ]



##########################################################
# # Con Clases
# class ApiClass:
#     def __init__(self, api_key, api_key_secret):
#         self.auth = tweepy.OAuthHandler(api_key, api_key_secret)
#         self.auth.set_access_token(acces_token, acces_token_secret)
#         self.api = tweepy.API(self.auth)
#
#     def reload(self):
#         return self.api
##########################################################