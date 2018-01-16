import urllib.request
import time
import os
import sqlite3
import sys
from sqlite3 import Error

# TODO collect_transactions() should take in a 'time' argument and should parse the transactions from that point,
# TODO (cont.) returning a list of transactions tuples in the proper format.

# TODO add method that takes a specified 'time' and runs collect_transactions on it, then finds where the transactions
# TODO (cont.) ended and calls collect_transactions on the last timestamp.  continues until total transactions returned
# TODO (cont.) is less than 500


def data_scraper():
    """Scrapes data from Gemini.

    Scrapes the most recent historical trade data that is available and not currently in our GeminiHistoricalData
    database, and adds that data to said database, which is used when backtesting our trading strategies.

    """
    # Make sure your GeminiHistoricalData database file is in the same directory as this file
    db_file = os.path.dirname(os.path.realpath(__file__)) + "\GeminiHistoricalData"
    conn = create_connection(db_file)
    (transactions, number_of_transactions) = collect_transactions()
    insert_transactions(conn, transactions)

    test_query(conn)

    print(number_of_transactions)

    conn.close()


def create_connection(database):
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)
        sys.exit(1)


def collect_transactions():
    transaction_list = [(12, 4, 1032, 9.9, 9.9, "sell"), (932, 4, 103323, 9.9, 9.9, "sell"), (9, 4, 10443, 923.9, 9.329, "sell"), (12, 4, 1032, 9.9, 9.9, "sell"), (932, 4, 103323, 9.9, 9.9, "sell"), (9, 4, 10443, 923.9, 9.329, "sell")]

    # date = int(time.mktime(time.strptime('2018-1-12 00:00:00', '%Y-%m-%d %H:%M:%S')))
    # response = urllib.request.urlopen("https://api.gemini.com/v1/trades/btcusd?timestamp=%s&limit_trades=500" % date)

    return transaction_list, len(transaction_list)


def insert_transactions(conn, transaction_list):
    sql = ''' INSERT OR IGNORE INTO GeminiTradeData (timestamp, timestampms, tid, price_usd, amount_btc, transaction_type) 
              VALUES (?, ?, ?, ?, ?, ?)'''

    cur = conn.cursor()
    cur.executemany(sql, transaction_list)

    conn.commit()


# this function is only for testing and development purposes
def test_query(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM GeminiTradeData")

    rows = cur.fetchall()

    for row in rows:
        print(row)


