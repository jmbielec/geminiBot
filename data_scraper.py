import urllib.request
import time
import os
import sqlite3
import sys
from sqlite3 import Error


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
    """Establishes a connection with the given sqlite database."""
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)
        sys.exit(1)


def collect_transactions(timestamp):
    """Collects Gemini trade transactions.

    This function returns a list of all trades/transactions made on Gemini for BTC/USD after the given timestamp
    up through the time when the function is called.

    :param timestamp: human readable timestamp (e.g. '2018-1-12 00:00:00')
    :return: returns the list of transactions in the form of tuples
            (eg. [(timestamp, timestampms, tid, price_usd, amount_btc, transaction_type)])

    """

    start_time = regular_to_epoch(timestamp)
    current_time = int(time.time())

    # TODO while greater than start_time and less that current_time, keeping adding transactions to transaction list
    # TODO the last page of transactions could be less than 500 so end after that or after current_time has been reached

    transaction_list = [(12, 4, 1032, 9.9, 9.9, "sell"), (932, 4, 103323, 9.9, 9.9, "sell"), (9, 4, 10443, 923.9, 9.329, "sell"), (12, 4, 1032, 9.9, 9.9, "sell"), (932, 4, 103323, 9.9, 9.9, "sell"), (9, 4, 10443, 923.9, 9.329, "sell")]

    # response = urllib.request.urlopen("https://api.gemini.com/v1/trades/btcusd?timestamp=%s&limit_trades=500" % date)

    return transaction_list, len(transaction_list)


def insert_transactions(conn, transaction_list):
    """Inserts rows of transactions to database.

    Inserts the entire list of transactions into the GeminiHistoricalDatabase, with the exception of
    transactions that already exist in the database as identified by their tid (transaction ID).

    """

    sql = ''' INSERT OR IGNORE INTO GeminiTradeData (timestamp, timestampms, tid, price_usd, amount_btc, transaction_type) 
              VALUES (?, ?, ?, ?, ?, ?)'''

    cur = conn.cursor()
    cur.executemany(sql, transaction_list)

    conn.commit()


def regular_to_epoch(timestamp):
    """Converts from human readable date to epoch date.

    :param timestamp: human readable timestamp (e.g. '2018-1-12 00:00:00')
    :return: epoch timestamp (e.g. 1515715200)

    """

    return int(time.mktime(time.strptime(timestamp, '%Y-%m-%d %H:%M:%S'))) - time.timezone


def epoch_to_regular(timestamp):
    """Converts from epoch to human readable date.

    :param timestamp: epoch timestamp (e.g. 1515715200)
    :return:  human readable timestamp (e.g. '2018-1-12 00:00:00')

    """

    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp))


# this function is only for testing and development purposes
def test_query(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM GeminiTradeData")

    rows = cur.fetchall()

    for row in rows:
        print(row)


