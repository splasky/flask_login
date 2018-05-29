#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2018-05-29 09:57:13

import logging
import sys
from flask import (Flask, request, render_template, redirect, url_for,
                   make_response)
from flask import json
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash


mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'aws_ubuntu'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
app.config['MYSQL_DATABASE_DB'] = 'Flask_DB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(
        filename, lineno, exc_type, exc_obj))


@app.route('/')
def main():
    user = request.cookies.get('user_name')
    return render_template('home.html', user=user)


@app.route('/showSignUp')
def showSignUp():
    user = request.cookies.get('user_name')
    return render_template('login.html', user=user)


@app.route('/showLogIn')
def showSignIn():
    user = request.cookies.get('user_name')
    return render_template('login.html', user=user)


@app.route('/logIn', methods=['POST'])
def signIn():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _name = request.form.get('inputName', None)
        _password = request.form.get('inputPassword', None)

        if _name and _password:
            _hashed_password = generate_password_hash(_password)
            cursor.execute('select user_name, user_password from Accounts where\
                           user_name={} and\
                           user_password={}'.format(_name, _hashed_password))
            data = cursor.fetchall()
        if len(data) is 0:
            message = json.dumps({'message': 'User login successfully!'})
            resp = make_response(redirect(url_for('index')), message)
            resp.set_cookie('user_name', _name)
            return resp
        else:
            message = json.dumps({'message': 'User login failed'})
            resp = make_response(redirect(url_for('index')), message)
            return resp

    except Exception as e:
        PrintException()
        return redirect(url_for('index'))
    finally:
        cursor.close()
        conn.close()


@app.route('/signUp', methods=['POST'])
def signUp():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        # read the posted values from the UI
        _name = request.form.get('inputName', None)
        _password = request.form.get('inputPassword', None)

        logging.debug("account:{_name} password:{_password}")
        # validate the received values
        if _name and _password:

            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                message = json.dumps({'message': 'User created successfully!'})
            else:
                message = json.dumps({'error': str(data[0])})
        resp = make_response(redirect(url_for('index')), message)
        resp.set_cookie('user_name', _name)
        return resp

    except Exception as e:
        PrintException()
        return redirect(url_for('index'))
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        app.run()
    except:
        PrintException()
