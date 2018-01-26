def trading_strats(strategy_name):
    if strategy_name == 'mean_reversion':
        mean_reversion()
    else:
        print('usage: trading_strats(strategy_name)')
        print('valid inputs for strategy_name: mean_reversion')


def mean_reversion():
    # TODO listen to voice recording on iphone about ideas for trading strats
    # TODO add parameters for when to buy, sell, stop loss, trailing stop loss, how long to precollect data, money to buy with

    data_list = [1.0] #TODO this is 15 minutes of price data, make it real
    price_list = [1.0, 3.0, 3.0, 1.9, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 1.8, 1.6, 0.9, 1.2, 1.3, 1.4, 1.5, 1.8, 1.7, 1.8, 1.9, 2.1, 1.8]
    price_sum = 0
    price_count = 0
    buy = True
    sell = False

    # TODO instead of two different lists and loops, make one list and check in loop for time lapse of 15 minutes before buying and selling
    for price in data_list:
        price_count += 1
        price_sum += price

    for price in price_list:
        price_count += 1
        price_sum += price
        price_average = price_sum / price_count
        if buy and price < price_average:
            print("Bought at:", price)
            buy = False
            sell = True
        elif sell and price > 1.9:
            print("Sold at:", price)
            buy = True
            sell = False
