#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 03 21:05:00 2021
@author: iv
"""


import sys
import requests as rq
import logging


## Logging
logging.basicConfig(format='%(asctime)s %(name)s-%(levelname)s:: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
cryptoRRSS_log = logging.getLogger("CryptoRRSS_Logging")
sys.stdout.flush()
cryptoRRSS_log.info(sys.platform + ' System')


def peticion_api(userid_list=None, count_twits=None, lang=None):
    # url = 'http://192.168.1.43:5000/api/v1/cryptorrss/sentiment?userid_list=CriptoNoticias-coingecko-CoinDesk&count_twits=4'
    url = 'http://192.168.1.43:5000/api/v1/cryptorrss/sentiment?'
    if userid_list is None:
        userid_list = input('Dame la lista de cuentas de twitter separadas con guiones medios: ')
        url_tot = url + 'userid_list=' + f'{userid_list}'
    else:
        url_tot = url + 'userid_list=' + f'{userid_list}'
    if count_twits is None:
        count_twits = input('Dime el numero de twitts a recopilar de cada cuenta: ')
        url_tot = url_tot + '&' + 'count_twits=' + f'{count_twits}'
    else:
        url_tot = url_tot + '&' + 'count_twits=' + f'{count_twits}'
    if lang is None:
        lang = input('Dime el idioma al que traducir todos los text ("en" por defecto): ')
        url_tot = url_tot + '&' + 'count_twits=' + f'{count_twits}' + '&' + 'lang=' + f'{lang}'
    else:
        url_tot = url_tot + '&' + 'count_twits=' + f'{count_twits}' + '&' + 'lang=' + f'{lang}'
    respuesta = rq.get(url_tot).json()
    print(respuesta)
    return respuesta


if __name__ == '__main__':
    peticion_api()
