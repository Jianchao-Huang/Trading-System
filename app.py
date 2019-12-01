from flask import Flask
from flask import render_template, redirect, url_for, request, flash, session, jsonify

import requests
import asyncio

import wtforms as wtf

import config
from functools import wraps


from passlib.hash import sha256_crypt
import gc


app = Flask(__name__)
app.secret_key = 'please-generate-a-random-secret_key'
#
# def verifySessionId():
#     global nextId
#
#     if not 'userId' in session:
#         session['userId'] = nextId
#         nextId += 1
#         sessionId = session['userId']
#         print ("set userid[" + str(session['userId']) + "]")
#     else:
#         print ("using already set userid[" + str(session['userId']) + "]")
#     sessionId = session.get('userId', None)
#     return sessionId


def mysql_connection():
    conn = mc.connect(host="127.0.0.1",
                      user="root",
                      password="malanming0OO0",
                      database="crypto",
                      auth_plugin='mysql_native_password',
                      buffered=True)
    cursor = conn.cursor()
    return cursor, conn


def marketData(currency):
    return requests.get('https://api.binance.com/api/v3/ticker/24hr?symbol=' + currency.upper()).json()

def candlestick(currency):
    return requests.get('https://api.binance.com/api/v3/klines?symbol=' + currency.upper() + '&interval=1d').json()

def weekData(currency):
    weekData = []
    for i in range(0,7):
        weekData.append(float(currency[493+i][4]))
    return weekData


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        cursor, conn = mysql_connection()
        input_email = request.form['email']
        input_password = request.form['password']
        cursor.execute(
            "SELECT password FROM users WHERE email = %s", (input_email,))
        password = str(cursor.fetchone()[0])
        cursor.close()
        conn.close()
        if input_password == password:
            return redirect(url_for('overview'))
        else:
            return 'Username does not exist or Password is wrong. Please try again.'
    return render_template('login.html')
#
# #
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('error.html')

#
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":

        register_email = str(request.form['register_email'])
        register_username = str(request.form['register_username'])
        register_password = str(request.form['register_password'])

        cursor, conn = mysql_connection()
        cursor.execute("SELECT * FROM users WHERE email = %s or username = %s",
                       (register_email, register_username,))
        duplicates = cursor.fetchall()

        if len(duplicates) > 0:
            flash("That email is already taken, please choose another")
            return render_template('register.html')
        else:
            sql = """INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"""
            val = (register_email, register_username, register_password)
            cursor.execute(sql, val)
            conn.commit()
            flash("Congratulations! You can now start trading.")
            return redirect(url_for('login'))
        cursor.close()
        conn.close()
    return render_template('register.html')


@app.route('/Trading', methods=["GET", "POST"])
def trading():
    return render_template('trading.html')


@app.route('/Overview')
def overview():
    BTC = marketData('btcusdt')
    ETH = marketData('ethusdt')   
    LTC = marketData('ltcusdt')
    BTCC = marketData('BCHBTC')
    XRP = marketData('xrpusdt')
    TRON = marketData('trxusdt')
    Bitcoin = candlestick('btcusdt')
    Ethrium = candlestick('ethusdt')
    Litecoin = candlestick('ltcusdt')
    BitCoinCash = candlestick('BCHBTC')
    XRP = candlestick('xrpusdt')
    TRON = candlestick('trxusdt')

    BitcoinWeekData = weekData(Bitcoin)
    EthriumWeekData = weekData(Ethrium)
    LitecoinWeekData = weekData(Litecoin)
    # BitCoinCashWeekData = weekData(BitCoinCash)
    XRPWeekData = weekData(XRP)
    TRONWeekData = weekData(TRON)

    class currencyData:
        def __init__(self, name, marketData, weekdata, imageName):
            self.name = name
            self.marketData = marketData
            self.weekdata = weekdata
            self.imageName = imageName

    BitcoinData = currencyData('Bitcoin', marketData('btcusdt'), BitcoinWeekData, 'btc')
    EthriumData = currencyData('Ethrium', marketData('ethusdt'), EthriumWeekData, 'eth')
    LitecoinData = currencyData('Litecoin', marketData('ltcusdt'), LitecoinWeekData, 'ltc')
    BitCoinCashData = currencyData('BitCoin Cash', marketData('BCHBTC'), '', 'btcc')
    XRPData = currencyData('XRP', marketData('xrpusdt'), XRPWeekData, 'xrp')
    TRONData = currencyData('TRON', marketData('trxusdt'), TRONWeekData, 'tron')
    currencies = [BitcoinData, EthriumData, LitecoinData, XRPData, TRONData, BitCoinCashData]


    return render_template('market-overview.html', len=len(currencies), currencies=currencies)

    

   


@app.route('/Account')
def account():
    return render_template('withdrawl.html')

@app.route('/_dataUpdate', methods = ['GET'])
def dataUpdate():
   
    
    return jsonify(result=time.time())

@app.route('/_stuff', methods = ['GET'])
def stuff():

    Bitcoin = candlestick('btcusdt')
    Ethrium = candlestick('ethusdt')
    Litecoin = candlestick('ltcusdt')
    BitCoinCash = candlestick('BCHBTC')
    XRP = candlestick('xrpusdt')
    TRON = candlestick('trxusdt')

    BitcoinWeekData = weekData(Bitcoin)
    EthriumWeekData = weekData(Ethrium)
    LitecoinWeekData = weekData(Litecoin)
    # BitCoinCashWeekData = weekData(BitCoinCash)
    XRPWeekData = weekData(XRP)
    TRONWeekData = weekData(TRON)

   
    return jsonify(
        BTC = marketData('btcusdt'),
        ETH = marketData('ethusdt'),   
        LTC = marketData('ltcusdt'),
        BTCC = marketData('BCHBTC'),
        XRP = marketData('xrpusdt'),
        TRON = marketData('trxusdt'),
        BitcoinWeekData = weekData(Bitcoin),
        EthriumWeekData = weekData(Ethrium),
        LitecoinWeekData = weekData(Litecoin),
        # BitCoinCashWeekData = weekData(BitCoinCash),
        XRPWeekData = weekData(XRP),
        TRONWeekData = weekData(TRON)
    )




if __name__ == '__main__':
    app.debug = True
    app.run()
