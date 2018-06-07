#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2018-06-07 15:50:38

import sys
from flask import (Flask, request, render_template, redirect, url_for,
                   make_response, flash)
from flask import json
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash
from config import app

mysql = MySQL()
app = Flask(__name__)
CORS(app)

# MySQL configurations
mysql.init_app(app)

handler = logging.FileHandler('/tmp/app.log', encoding='UTF-8')
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)


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
    return render_template('signup.html', user=user)


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
            cursor.execute("select user_name, user_password from Accounts where\
                           user_name='{}' and\
                           user_password='{}';".format(_name, _hashed_password))
            data = cursor.fetchall()
            if len(data) is 0:
                message = json.dumps({'status': 200})
                return message
                #  resp = make_response(redirect(url_for('main')), message)
                #  resp.set_cookie('user_name', _name)
                #  app.logger.debug(message)
                #  return resp

        error = 'User accounts or password failed'
        app.logger.debug(message)
        return render_template('login.html', error=error)

    except:
        PrintException()
        return redirect(url_for('main'))
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

        # validate the received values
        if _name and _password:

            _hashed_password = generate_password_hash(_password)
            cursor.execute("INSERT Accounts(user_name,user_password)\
                    values('{}','{}');".format(
                _name, _hashed_password))
            conn.commit()
            message = json.dumps({'status': 200})
            return message
            #  resp = make_response(redirect(url_for('main')), message)
            #  resp.set_cookie('user_name', _name)
            #  return resp

        error = 'User accounts or password failed'
        app.logger.debug(message)
        return render_template('signup.html', error=error)

    except:
        PrintException()
        app.logger.info(
            "insert values {} {} failed".format(_name, _hashed_password))
        return redirect(url_for('main'))
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(port=5000)
