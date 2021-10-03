#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 03 21:05:00 2021
@author: iv
"""
import sys
import os
import pandas as pd
import json
import glob
from flask import Flask, jsonify
import logging
import yaml

### MODIFICAR CUANDO TOQUE
# print('Poner en el navegador "http://localhost:5000/api/v1/premios/bbdd/<numero1-numero2-...etc> or http://localhost:5000/api/v1/premios/csv/<numero1-numero2-...etc>" donde los numeros van separados por guiones')
# print('Poner en el navegador "http://Iv36.pythonanywhere.com/api/v1/premios/csv/<numero1-numero2-...etc> or http://Iv36.pythonanywhere.com/api/v1/premios/bbdd/<numero1-numero2-...etc> " donde los numeros van separados por guiones')
# print('Tambien desde una consola python "request.get("http://localhost:5000/api/v1/premios/<numero1-numero2-...etc>")", donde los numeros van separados por guiones')
# print('Pulsar ctrl+c para cancelar')


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
## Importar Parametros
with open('parameters.yaml', 'r') as parameters_file:
    param = yaml.safe_load(parameters_file)
    parameters_file.close()
crypto_trading_db = param['crypto_trading_db']
whatsapp_twilio_db = param['whatsapp_twilio_db']
mail_db = param['mail_db']
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




##### INICIO #####
## Creacion de la app
app = Flask(__name__) 

@app.route('/api/v1/cryptorrss/sentiment/<interval_time>', methods=['GET'])
def api_cryptosentiment(interval_time):
    # varias_operaciones
    # conexion_twitter
    # bajar_mensajes
    # conexion_otras_apps
    # bajar_mensajes
    # unir_todos_mensajes_segun_interval_time
    # aplicar_modelo_pickle_sentiment a los mensajes concatenados o por separado
    # lista_numeros = str_numeros.split('-')
    # dicc = {item:{'premio':suma_premios, 'causa':causa}}
    # lista_results.append(dicc)
    predict = {'prob_positive': 0.6,
               'prob_negative': 0.2,
               'prob_neutral': 0.2}
    return jsonify(predict)


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
