import urllib.request
import time

# TODO connect to database, find latest added timestamp, find transaction AFTER that timestamp, add them to database,
# TODO (cont.) close database


def data_scraper():
    """Scrapes data from Gemini.

    Scrapes the most recent historical trade data that is available and not currently in our GeminiHistoricalData
    database, and adds that data to said database, which is used when backtesting our trading strategies.

    """
    date = int(time.mktime(time.strptime('2018-1-12 00:00:00', '%Y-%m-%d %H:%M:%S')))
    response = urllib.request.urlopen("https://api.gemini.com/v1/trades/btcusd?timestamp=%s&limit_trades=500" % date)
    print(response.read())