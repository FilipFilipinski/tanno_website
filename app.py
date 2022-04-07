from flask import Flask, render_template
import requests
import sqlite3

nanopool_id = '0x4fcca869dd1dbadd57dfbbcb317410e39a0b0745'
worker_id = 'Nikaragua'

app = Flask(__name__)

'''The function takes the value of an account on a nanopool
and returns its contents in the form of the quantity ETH'''


def balance_eth() -> str:
    link = f'https://api.nanopool.org/v1/eth/balance/{nanopool_id}'
    response = str(requests.get(link).json()['data'])
    return response


'''️Function retrieves current ETH value in USD from API
www.cryptocompare.com'''


def eth_currency_price_usd() -> str:
    link = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD'
    response = requests.get(link).json()['USD']
    return response


'''️The function gets the value of the account on the nanopool
and returns its contents in the form of the number of USD'''


def balance_usd() -> str:
    eth_usd = float(eth_currency_price_usd())
    bal_eth = float(balance_eth())
    response = str(round(eth_usd * bal_eth, 2))
    return response


'''Function returns the average value of the 168
previous hours (7 days) of hashrate️️'''


def hashrate() -> str:
    link = f'https://api.nanopool.org/v1/eth/avghashratelimited/{nanopool_id}/{worker_id}/168'
    response = str(round(requests.get(link).json()['data'], 2))
    return response


'''function returns dictionary arrays which contain in sequence
values: minute, hour, day, month along with calculated earnings
from average hash of last 7 days️️'''


def calculator() -> list:
    response = []
    link = 'https://api.nanopool.org/v1/eth/approximated_earnings/'
    for i in ['minute', 'hour', 'day', 'week', 'month']:
        response.append({i: round(requests.get(link + hashrate()).json()['data'][i]['dollars'], 2)})
    return response


@app.route('/')
def main():
    conn = sqlite3.connect('nano.db')
    c = conn.cursor()
    c.execute("SELECT * FROM nano")
    page = c.fetchall()
    return render_template('index.html', my_eth=page[0][1], month=page[1][1], day=page[2][1], id=nanopool_id)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
