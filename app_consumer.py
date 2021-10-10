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


def peticion_api(time_period=None):
    url = 'http://iv36.pythonanywhere.com/api/v1/cryptorrss/sentiment/'
    if time_period is None:
        time_period = input('Dame el timeperiod en dias: ')
        respuesta = rq.get(url+f'{time_period}').json()
    else:
        respuesta = rq.get(url+f'{time_period}').json()
    print(respuesta)
    return respuesta


if __name__ == '__main__':
    peticion_api()

## END ##