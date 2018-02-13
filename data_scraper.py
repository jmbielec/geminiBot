import urllib.request
import time
import os
import sqlite3
import sys
import re
from sqlite3 import Error


def data_scraper():
    """Scrapes data from Gemini.

    Scrapes the most recent historical trade data that is available and not currently in our GeminiHistoricalData
    database, and adds that data to said database, which is used when backtesting our trading strategies.

    """
    print('Connecting to database...')
    # Make sure your GeminiHistoricalData database file is in the same directory as this file
    db_file = os.path.dirname(os.path.realpath(__file__)) + "\GeminiHistoricalData"
    conn = create_connection(db_file)
    print('Database connected.')

    print('Collecting and inserting transactions...')
    end_transaction_time = int(time.time())
    (transactions, number_of_transactions, last_transaction_time) = collect_transactions(int(time.time()) - 345600)
    insert_transactions(conn, transactions)

    while number_of_transactions == 500 and end_transaction_time > last_transaction_time:
        (transactions, number_of_transactions, last_transaction_time) = collect_transactions(last_transaction_time)
        insert_transactions(conn, transactions)

    print('Transactions collected and inserted.')

    print('Disconnecting from database...')
    conn.close()
    print('Database disconnected.')
    return "Scraping finished!"


def create_connection(database):
    """Establishes a connection with the given sqlite database."""
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)
        sys.exit(1)


def collect_transactions(epoch_start_time):
    """Collects Gemini trade transactions.

    This function returns a list of all trades/transactions made on Gemini for BTC/USD after the given timestamp
    up through the time when the function is called.

    :param epoch_start_time: takes the epoch timestamp from four days ago during the current time by subtracting 3456python00
    :return: returns the list of transactions in the form of tuples
            (eg. [(timestamp, timestampms, tid, price_usd, amount_btc, transaction_type)])

    """

    response = urllib.request.urlopen("https://api.gemini.com/v1/trades/btcusd?timestamp=%s&limit_trades=500" % epoch_start_time)
    encoded_transactions = response.read()
    decoded_transactions = encoded_transactions.decode()

    parsed_transactions = re.findall(r'{"timestamp":(\d+),"timestampms":(\d+),"tid":(\d+),"price":"(\d+\.?\d*)","amount":"(\d+\.?\d*)","exchange":"gemini","type":"(\w+)"}', decoded_transactions)

    transaction_list = []
    for transaction in parsed_transactions:
        (timestamp, timestampms, tid, price_usd, amount_btc, transaction_type) = transaction
        transaction_list.append((int(timestamp), int(timestampms), int(tid), float(price_usd), float(amount_btc), transaction_type))

    (last_transaction_time, _, _, _, _, _) = transaction_list[0]

    return transaction_list, len(transaction_list), last_transaction_time


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
