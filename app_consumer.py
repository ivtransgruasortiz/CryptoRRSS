# # -*- coding: utf-8 -*-
# """
# Created on Sat Dec 12 17:41:19 2020
#
# @author: iv
# """
#
#
# ###############################
# ## SELECT PLATFORM: ##########
# #############################
# ###-- WINDOWS OR LINUX --###
# ###########################
# import sys
# if sys.platform == 'win32':
#     path = ''
#     print ('\n#### Windows System ####')
#     system = sys.platform
# else:
#     path = ''
#     print ('\n#### Linux System ####')
#     system = sys.platform
#
# print ('#####################################')
# print ('#####################################')
# print ('\n### Importing Libraries... ###')
#
# import os
# import pandas as pd
# import numpy as np
# import requests as rq
# import csv
# import json
# import glob
# import pymongo
# from flask import Flask, request, render_template, jsonify
#
# #import time
# #import datetime
# #import pylab as pl
# #import seaborn as sns
# #import matplotlib as mpl
# #import matplotlib.pyplot as plt
# #import lxml
# #import urllib
# #import statsmodels
# #import sklearn
# #import nltk
# #import scipy
# #import tables
# #import json, hmac, hashlib, time, requests, base64
# #from requests.auth import AuthBase
# #import datetime as dt
# #import timeit
# #import math
# #from scipy import stats
# #import base64
# #import pyspark
# #from pyspark import SparkConf, SparkContext
# #from pyspark.sql import SparkSession
# #print(os.path.dirname(os.path.realpath(__file__)))
#
#
# if '__file__' in locals():
#     wd = os.path.dirname(__file__)
#     sys.path.append(wd)
#     sep = '/'
# else:
#     wd = os.path.abspath('./Documents/Repositorio_Iv/premios_loteria/working_folder/app/')
#     wd = wd + '/'
#     sys.path.append(wd)
#     sep = '/'
#
# def peticion_api(lista_str=None):
#     # url = 'http://localhost:5000/api/v1/premios/bbdd/'
#     url = 'http://iv36.pythonanywhere.com/api/v1/premios/csv/'
#     if lista_str == None:
#         lista_str = input('Dame la lista de numeros a comprobar separados por guiones sin espacios: ')
#         respuesta = rq.get(url+f'{lista_str}').json()
#     else:
#         respuesta = rq.get(url+f'{lista_str}').json()
#     # print(respuesta)
#     for item in respuesta:
#         for numero, premio in item.items():
#             numero = numero
#             cantidad = premio['premio']
#             causa = premio['causa']
#             causa = str.replace(causa, '-', ', ')
#             if cantidad == '0':
#                 print(f'El número {numero} no está premiado')
#             else:
#                 print(f'El número {numero} está premiado con  --> {cantidad} euros y acumula los siguientes premios: {causa}')
#     return respuesta
#
#
# if __name__ == '__main__':
#     peticion_api()
#
# ## END ##