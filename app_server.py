#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 03 21:05:00 2021
@author: iv
"""
import sys
import os
import pandas as pd
import yaml
import tweepy
import ssl
import pymongo
import flask
import logging
from app_twitterconnect import json_sentiment


### MODIFICAR CUANDO TOQUE
print('### Examples ###')
print('Poner en el navegador "http://192.168.1.43:5000/api/v1/cryptorrss/sentiment?userid_list=<CriptoNoticias-coingecko-CoinDesk>&count_twits=<4>"')
print('Poner en el navegador "http://Iv36.pythonanywhere.com/api/v1/cryptorrss/sentiment?userid_list=<CriptoNoticias-coingecko-CoinDesk>&count_twits=<4>"')
print('Tambien desde una consola python "request.get("http://localhost:5000/api/v1/cryptorrss/sentiment?userid_list=<CriptoNoticias-coingecko-CoinDesk>&count_twits=<4>")"')
print('Press ctrl+c to cancel')


## Logging
logging.basicConfig(format='%(asctime)s %(name)s-%(levelname)s:: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
cryptoRRSS_log = logging.getLogger("CryptoRRSS_Logging")
sys.stdout.flush()
print('#####################################')
cryptoRRSS_log.info(sys.platform + ' System')

### SYSTEM DATA ###
if '__file__' in locals():
    if locals()['__file__'] == '<input>':
        wd = os.path.split(os.path.realpath(__file__))[0]
        wd += '/'
        sys.path.append(wd)
        os.chdir(wd)
        del locals()['__file__']
    else:
        wd = os.path.dirname(__file__)
        wd += '/'
        sys.path.append(wd)
        os.chdir(wd)
else:
    wd = os.path.abspath("./Documents/Repositorio_Iv/CryptoRRSS")
    wd += '/'
    sys.path.append(wd)
if sys.platform == 'win32':
    system = sys.platform
else:
    system = sys.platform


if '__file__' in locals():
    client_r = pymongo.MongoClient(
        "mongodb+srv://%s:%s@cluster0.vsp3s.mongodb.net/" % (sys.argv[1], sys.argv[2]), ssl_cert_reqs=ssl.CERT_NONE)
    twitter_db = 'twitter_db'
    db_twitter = client_r.get_database(twitter_db)
    twitter_records = db_twitter.credentials_data_records
    twitter_data = list(twitter_records.find({}, {"_id": 0}))
    auth_tweeter = twitter_data[0]
    print('__file__' in locals())
    print('Vamos por el buen camino...')
else:
    with open("config.yaml", "r") as stream:
        auth_tweeter = yaml.safe_load(stream)
        stream.close()


# Pandas options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# User and password for twitter account
api_key = auth_tweeter['api_key']
api_key_secret = auth_tweeter['api_key_secret']
acces_token = auth_tweeter['acces_token']
acces_token_secret = auth_tweeter['acces_token_secret']
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(acces_token, acces_token_secret)
api = tweepy.API(auth)



##### INICIO #####
## Creacion de la app
app = flask.Flask(__name__)

@app.route('/api/v1/cryptorrss/sentiment/', methods=['GET'])
def api_cryptosentiment():
    userid_list = flask.request.args.get('userid_list', None)
    count_twits = flask.request.args.get('count_twits', None)
    userid_list = userid_list.split('-')
    predict = json_sentiment(api, userid_list=userid_list, count_twits=count_twits)
    return flask.jsonify(predict)


###############################################################################################################
#         INFINITY LOOP LISTENING TO PORT 80 (port=int("80")) TO THE OUTSIDE WORLD (host="0.0.0.0") - START   #
###############################################################################################################


app.config['JSON_AS_ASCII'] = False
if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(
            host="0.0.0.0",
            port=int("5000")
    )  # Puerto "80" para pythonanywhere


###############################################################################################################
#         INFINITY LOOP LISTENING TO PORT 80 (port=int("80")) TO THE OUTSIDE WORLD (host="0.0.0.0") - END     #
###############################################################################################################
#
