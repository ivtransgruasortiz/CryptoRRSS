#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 03 21:05:00 2021
@author: iv
"""
import sys
import os
import pandas as pd
import numpy as np
from textblob import TextBlob
import re
from textblob.sentiments import NaiveBayesAnalyzer
from googletrans import Translator
import unicodedata


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


def get_name(x):
    result = x['screen_name']
    return result


def sent_analisys(x):
    blob_object = TextBlob(x, analyzer=NaiveBayesAnalyzer())
    analysis = blob_object.sentiment
    analysis = '$'.join([str(x) for x in analysis])
    return analysis


def filtertext(x, excel_file):
    df_palabras = pd.read_excel(wd + excel_file)
    df_palabras = df_palabras.fillna(0)
    lista_words = list(df_palabras['PALABRAS'].values) + \
                  list(df_palabras['hastag'].values) + \
                  list(df_palabras['arroba'].values)
    # lista_words = list(filter((0).__ne__, lista_words))  #Tambien nos valdria
    lista_words = [x for x in lista_words if x != 0]
    result = []
    for word in lista_words:
        tag = bool(re.search(word, x.lower()))
        result.append(tag)
    return max(result)


def translate_en(x, lang='en'):
    translator = Translator()
    result = translator.translate(x, dest=lang).text
    return result


def cleantext(x):
    result = unicodedata.normalize('NFD', x).encode("utf8").decode("ascii", "ignore")
    result = re.sub('[%+\\\+\(+\)+&+\n+\r+./]', ' ', result)
    result = re.sub(' +', ' ', result)
    result = result.strip()
    return result


# userid_list = ('CriptoNoticias', 'bit2me', 'MundoCrypto_ES', 'Tesla',
#                'cryptocom', 'elonmusk', 'nayibbukele', 'Cointelegraph', 'crypto', 'CoinMarketCap',
#                'ForbesCrypto', 'CryptoBoomNews', 'BTCTN', 'solana', 'CoinbasePro', 'coingecko', 'CoinDesk',
#                'blockchain', 'healthy_pockets', 'wallstwolverine'
#                )

userid_list = ('CriptoNoticias', 'coingecko', 'CoinDesk', 'blockchain', 'MundoCrypto_ES', 'bit2me', 'healthy_pockets',
               'wallstwolverine', 'elonmusk', 'cryptocom', 'CryptoBoomNews', 'Cointelegraph', 'crypto', 'CoinMarketCap'
               )


def json_sentiment(api, userid_list=userid_list, count_twits=3):
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
    twits_df['full_text'] = np.vectorize(cleantext)(twits_df['full_text'])
    twits_df['has_keys'] = np.vectorize(filtertext)(twits_df['full_text'], 'Palabras_Crypto.xlsx')
    twits_df = twits_df[twits_df['has_keys'] == True]
    twits_df_en = twits_df[twits_df['lang'] == 'en'].reset_index()
    twits_df_others = twits_df[twits_df['lang'] != 'en'].reset_index()
    twits_df_others['full_text'] = np.vectorize(translate_en)(twits_df_others['full_text'])
    twits_df = pd.concat([twits_df_en, twits_df_others])
    twits_df['username'] = np.vectorize(get_name)(twits_df['user'])
    twits_df = twits_df.reset_index()
    twits_df['result'] = np.vectorize(sent_analisys)(twits_df['full_text'])
    twits_df['result2'] = twits_df['result'].str.split('$')
    twits_df['sent_analisys_result'] = np.vectorize(lambda x: x[0])(twits_df['result2'])
    twits_df['sent_analisys_pos'] = np.vectorize(lambda x: float(x[1]))(twits_df['result2'])
    twits_df['sent_analisys_neg'] = np.vectorize(lambda x: float(x[2]))(twits_df['result2'])
    twits_df = twits_df[['id', 'full_text', 'lang', 'has_keys', 'username', 'sent_analisys_result', 'sent_analisys_pos',
                         'sent_analisys_neg']]
    media_pos = round(twits_df['sent_analisys_pos'].mean(), 4)
    media_neg = round(twits_df['sent_analisys_neg'].mean(), 4)
    media_str = 'pos' if media_pos > media_neg else 'neg'
    result = {'prob_positive': media_pos,
              'prob_negative': media_neg,
              'prob_conclusion': media_str,
              'TWITTS_positive_max': str(twits_df[twits_df['sent_analisys_pos'] ==
                                                  twits_df['sent_analisys_pos'].max()]['full_text'].item()),
              'TWITTS_negative_max': str(twits_df[twits_df['sent_analisys_neg'] ==
                                                  twits_df['sent_analisys_neg'].max()]['full_text'].item())
              }
    return result


### PRUEBAS #############################################################
# prueba = json_sentiment(api, userid_list=userid_list, count_twits=3)

# ##### TRADUCTOR #######################################################
# ### GoogleTrans
# text = 'Hola'
# from googletrans import Translator
# translator = Translator()
# translator.translate(text, dest='en').text
# translator.translate(text).text
#
# ### TextBlob
# from textblob import TextBlob
# blob = TextBlob('comment ca va ?')
# blob.translate(to='en')
#
# ### Translate
# from translate import Translator
# translator = Translator(to_lang="zh")
# translation = translator.translate("This is a pen.")
# ##### FIN ############################################################