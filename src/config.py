#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2018-06-07 15:35:51

from flask import Flask
from flask_cors import CORS
import logging

app = Flask(__name__)
app.jinja_env.globals['WEB_SERVER'] = "http://"
app.jinja_env.globals['APP_SERVER'] = "http://"
CORS(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Flask_DB'
app.config['MYSQL_DATABASE_HOST'] = ''

app.secret_key = ""
handler = logging.FileHandler('/tmp/app.log', encoding='UTF-8')
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
