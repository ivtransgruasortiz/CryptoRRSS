#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 03 21:05:00 2021
@author: iv
"""


import sys
import os
import requests as rq
import logging


## Logging
logging.basicConfig(format='%(asctime)s %(name)s-%(levelname)s:: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
cryptoRRSS_log = logging.getLogger("CryptoRRSS_Logging")
sys.stdout.flush() #Para cambiar el comportamiento de los print -- sin esta línea los escribe del tirón...
print('#####################################')
cryptoRRSS_log.info(sys.platform + ' System')
print('#####################################')
cryptoRRSS_log.info('### Importing Libraries... ###')
# ## Importar Parametros
# with open('parameters.yaml', 'r') as parameters_file:
#     param = yaml.safe_load(parameters_file)
#     parameters_file.close()
# crypto_trading_db = param['crypto_trading_db']
# whatsapp_twilio_db = param['whatsapp_twilio_db']
# mail_db = param['mail_db']


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


def peticion_api(userid_list=None, count_twits=None):
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
    respuesta = rq.get(url_tot).json()
    print(respuesta)
    return respuesta


if __name__ == '__main__':
    peticion_api()

## END ##