from keys import client

def print_start():
    print("""
_________________________________________________________________________________________________________________________________   
     _____         /\  \         /\__\         /\__\                         /\  \                       /\__\         /\  \    
    /::\  \       /::\  \       /:/ _/_       /:/ _                         /::\  \                     /:/ _/_       /::\  \   
   /:/\:\  \     /:/\:\  \     /:/ /\  \     /:/ /\__                      /:/\:\  \                   /:/ /\  \     /:/\:\  \  
  /:/  \:\__\   /:/  \:\  \   /:/ /::\  \   /:/ /:/ _/_                   /:/ /::\  \   ___     ___   /:/ /::\  \   /:/  \:\  \ 
 /:/__/ \:|__| /:/__/ \:\__\ /:/__\/\:\__\ /:/_/:/ /\__\                 /:/_/:/\:\__\ /\  \   /\__\ /:/__\/\:\__\ /:/__/ \:\__\ 
 \:\  \ /:/  / \:\  \ /:/  / \:\  \ /:/  / \:\/:/ /:/  /                 \:\/:/  \/__/ \:\  \ /:/  / \:\  \ /:/  / \:\  \ /:/  /
  \:\  /:/  /   \:\  /:/  /   \:\  /:/  /   \::/_/:/  /                   \::/__/       \:\  /:/  /   \:\  /:/  /   \:\  /:/  / 
   \:\/:/  /     \:\/:/  /     \:\/:/  /     \:\/:/  /                     \:\  \        \:\/:/  /     \:\/:/  /     \:\/:/  /  
    \::/  /       \::/  /       \::/  /       \::/  /                       \:\__\        \::/  /       \::/  /       \::/  /   
     \/__/         \/__/         \/__/         \/__/                         \/__/         \/__/         \/__/         \/__/    
____________________________________________________________________________________________________________________________________                                                                                                                                
Run this garbage at your own risk , it will probably lose money.
Running Algorithm....   
_____________________________________________________________________ 

Saved Price | Last Price | % Change | Streak 
______________________________________________""")

def get_midpoint(ticker):
    OB = client.futures_order_book(symbol=ticker)
    midpoint = (float(OB['asks'][0][0]) + float(OB['bids'][0][0]))/2
    return midpoint

def get_account_value():
    av = client.futures_account_balance()
    #print(av[1]['asset'] , float(av[1]['balance']))
    return(float(av[1]['balance']))

def get_position(ticker):
    positions = client.futures_position_information()
    for position in positions:
        if position['symbol'] == ticker:
           # print(position)
            return({'position size' :float(position['positionAmt']) , 'mark price': float(position['markPrice'])})
        else:
            pass

def check_streak(current_price, last_price, minimum_move):
    if current_price < last_price * (1 + (minimum_move)) and current_price > last_price * (1 - minimum_move):
        return False
    else:
        return True

def return_streak(current_price , last_price , minimum_move , streak):
    if current_price > last_price * ( 1 + minimum_move):
        if streak < 1:
            new_streak = 1
            print("streak direction change new streak = " + str(new_streak), ' | ', last_price, ' | ', current_price)

        else:
            new_streak = streak + 1
            print("new streak = " + str(new_streak) ,' | ' , last_price ,' | ' , current_price)

    elif current_price < last_price * (1 - minimum_move):
        if streak > -1:
            new_streak = -1
            print("streak direction change new streak = " + str(new_streak) ,' | ' , last_price ,' | ' , current_price)

        else:
            new_streak = streak -1
            print("new streak = " + str(new_streak))

    return new_streak
