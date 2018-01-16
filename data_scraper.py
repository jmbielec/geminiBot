import urllib.request
import time
import os
import sqlite3
from sqlite3 import Error

# TODO connect to database, find latest added timestamp, find transaction AFTER that timestamp, add them to database,
# TODO (cont.) close database


class DataScraper:
    """Scrapes data from Gemini.

    Scrapes the most recent historical trade data that is available and not currently in our GeminiHistoricalData
    database, and adds that data to said database, which is used when backtesting our trading strategies.

    """
    def __init__(self):
        self.database = os.path.dirname(os.path.realpath(__file__)) + "\GeminiHistoricalData"
        self.conn = None

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.database)
            return self.conn
        except Error as e:
            print(e)
        return None

    def insert_transaction(self, transaction):
        sql = ''' INSERT OR IGNORE INTO GeminiTradeData (timestamp, timestampms, tid, price_usd, amount_btc, transaction_type) 
                  VALUES (?, ?, ?, ?, ?, ?)'''

        cur = self.conn.cursor()
        cur.execute(sql, transaction)


        self.conn.commit()
        return cur.lastrowid

    def test_query(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM GeminiTradeData")

        rows = cur.fetchall()

        for row in rows:
            print(row)

"""
def package_transaction():


def data_scraper():
    # Make sure your GeminiHistoricalData database file is in the same directory as this file

    date = int(time.mktime(time.strptime('2018-1-12 00:00:00', '%Y-%m-%d %H:%M:%S')))
    response = urllib.request.urlopen("https://api.gemini.com/v1/trades/btcusd?timestamp=%s&limit_trades=500" % date)
    
    """
