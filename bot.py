import sys
from data_scraper import data_scraper
from trading_strats import trading_strats


"""Trading Bot for Gemini Exchange

This is the main file for the bot, where data scraping, back testing, and live trading is conducted from.

"""


def main():
    """Takes a command line argument.

    Command line arguments:
    --scrape   --  scrapes the Gemini exchange to add trades to our GeminiHistorical Data sqlite database.
    --backtest --  runs a back test of our current trading strategy to test for profitability
    --live     --  starts the bot on the real exchange

    """
    if len(sys.argv) != 2:
        print('usage: python bot.py [--scrape | --backtest | --live]')
        sys.exit(1)

    option = sys.argv[1]

    if option == '--backtest':
        trading_strats('mean_reversion')
    elif option == '--live':
        print('this bot is currently not able to go live')
    elif option == '--scrape':
        print('Starting scraper...')
        print(data_scraper())
    else:
        print('unknown option:', option[0])
        print('usage: python bot.py [--scrape | --backtest | --live]')
        sys.exit(1)


if __name__ == '__main__':
    main()