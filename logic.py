import time
import math
from keys import client
import functions

depth = client.get_order_book(symbol='DOGEUSDT')
ticker = 'DOGEUSDT'
minimum_move = 0.01
allocation_long = 100 # % of account value to yeet into long
last_price = 0
streak = 0
while True:
    ### check if we have any data prior to running
    if last_price == 0:
        last_price = functions.get_midpoint(ticker)
        functions.print_start()

    current_price = functions.get_midpoint(ticker)

    if functions.check_streak(current_price , last_price , minimum_move) == False:
        print(f'{round(last_price , 5):.5f}' ,' | ' , f'{round(current_price , 5):.5f}' ,' | ' ,
              f'{round((current_price - last_price) / last_price , 5):.5f}' ,' | ' ,  f'{streak:.1f}')
        pass

    else:
        streak = functions.return_streak(current_price , last_price , minimum_move , streak)
        print("new streak is = " + str(streak))
        last_price = current_price
        position = functions.get_position(ticker)
        account_value = functions.get_account_value()
        current_price = functions.get_midpoint(ticker)
        order_size_long = math.floor((account_value * (allocation_long /100)) / current_price)
        order_size_usdt = (order_size_long * current_price)
        print("The current position is " + str(position['position size']))

        if position['position size'] == 0:
            if streak < -3 and order_size_usdt >= 5:
                client.futures_create_order(
                    symbol=ticker,
                    side='BUY',
                    type='MARKET',
                    quantity= order_size_long
                )
                print("submitted DOGEUSDT BUY order of " + str(order_size_long))

            elif streak < -3 and order_size_usdt < 5:
                print("Could not submit buy the minimum order needs to be at least 5usdt nerd")

            else:
                pass

        else:
            if position['position size'] > 0:
                if streak >= -3:
                    client.futures_create_order(
                        symbol=ticker,
                        side='SELL',
                        type='MARKET',
                        quantity=position['position size'],
                    )
                    print("submitted DOGEUSDT sell order of " + str(position['position size']))

    time.sleep(5)
