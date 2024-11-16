from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
import re
import json
from datetime import datetime, timedelta
import time
import logging
import numpy as np

# Load the JSON file
with open('cdp_api_key.json', 'r') as file:
    data = json.load(file)
api_key = data["name"]
api_secret = data["privateKey"]

class History():
    """ Gets data and returns signal. """
    def __init__(self):
        self.pc = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)
        self.avg1 = 50
        self.avg2 = 100

    def signal(self):
        self.startdate = (datetime.now() - timedelta(seconds=60*60*200)).strftime("%Y-%m-%dT%H:%M")
        self.enddate = datetime.now().strftime("%Y-%m-%dT%H:%M")

        self.data = self.pc.get_public_candles(
            'BTC-USD', 
            start=self.startdate, 
            end=self.enddate, 
            granularity=3600
        )
        
        self.data.sort(key=lambda x: x[0])
        
        if np.mean([x[4] for x in self.data[-self.avg1:]]) > np.mean([x[4] for x in self.data[-self.avg2:]]):
            return True
        else:
            return False

class Account():
    """ Authenticates, checks balances, places orders. """
    def __init__(self, order_limit):
        self.auth_client = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)
        self.size = order_limit
        
    def is_balanceUSD(self):
        self.balance = self.auth_client.get_crypto_balance("USDC")
        if self.balance and not self.balance.is_zero():
            return True
        return False
        
    def is_balanceBTC(self):
        self.balance = self.auth_client.get_crypto_balance("BTC")
        if self.balance and not self.balance.is_zero():
            return True
        return False
        
    def buy(self):
        return self.auth_client.fiat_market_buy(
            'BTC-USDC', 
            size=self.size
        )
        
    def sell(self):
        return self.auth_client.fiat_market_sell(
            'BTC-USD', 
            size=self.size
        )

client = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)

while(1):
    # exit condition
    cont = False
    while(cont == False):
        print("Do you want to close the server? Waiting...")
        user_input = input("Please enter 'y' or 'n': ").lower()
        if user_input == "y":
            exit()
        elif user_input == "n":
            cont = True
        else:
            print("Invalid input. Only 'y' or 'n' are allowed.\n")
            
    # First, see what account holdings we're working with
    print("\nYour current relevant holdings")
    client.get_crypto_balance('USDC')
    client.get_crypto_balance('BTC')

    # Now since we showed what we got, determine if we want to buy today
    run = False
    cont = False
    while(cont == False):
        print("\nDo you want to run the bot? Waiting...")
        user_input = input("Please enter 'y' or 'n': ").lower()
        if user_input == "y":
            run = True
            cont = True
        elif user_input == "n":
            print("Timing out until next hour, or until restart.\n")
            cont = True
            time.sleep((60*60) - datetime.now().minute*60 - (datetime.now().microsecond/1000000))
        else:
            print("Invalid input. Only 'y' or 'n' are allowed.\n")
            
    # Run bot trading algorithm
    if(run):
        logging.basicConfig(filename='./server.log', format='%(name)s - %(message)s')
        logging.warning('{} logging started'.format(datetime.now().strftime("%x %X")))
        
        # Algorithm to trade BTC with USDC
        def run():
            print('\nInitiating run(). Check log for details.')
            """ Order limit in USD for buys and sells. """
            cont = False
            order_limit = 0
            while(cont == False):
                print("What amount (USD) are you willing to buy? Waiting...")
                try:
                    user_input = float(input("Please enter a whole number dollar value (0, 5, 10, ect): "))
                    order_limit = user_input
                    cont = True
                except ValueError:
                    print("Invalid input! Please enter a valid decimal number.")
                
            auth_client = Account(order_limit=order_limit)
            if History().signal:
                if auth_client.is_balanceUSD():
                    cont = False
                    while(cont == False):
                        choice = input("Suggested to buy BTC . Continue? 'y' or 'n': ").lower()
                        if choice == "y":
                            # Next project is to look at the actual value of BTC. If its change in value from a certain time period ago to now is a certain percentage of its value now ((old - new)/new
                            # History signal is the market vector direction (inc., dec. in value) while this project will introduce magnitude of market vector gains
                            # 
                            # if value from a [timeperiod] ago is >= [percentage] greater than today
                            #   buy
                            # else
                            #   do nothing, the gain potential isnt that good
                            # 
                            # 
                            # )
                            buy = auth_client.buy()
                            logging.warning('{} - {}'.format(datetime.now(), buy)) 
                            print("Order status logged.")
                            cont = True
                        elif choice == "n":
                            print("Skipping buy order.")
                            cont = True
                        else:
                            ("Invalid input. Only 'y' or 'n' are allowed.")
            else:
                if auth_client.is_balanceBTC():
                    cont = False
                    while(cont == False):
                        choice = input("Suggested to sell BTC. Continue? 'y' or 'n': ").lower()
                        if choice == "y":
                            # Next project is to look at the actual value of BTC. If its change in value from a certain time period ago to now is a certain percentage of its value now ((old - new)/new
                            # History signal is the market vector direction (inc., dec. in value) while this project will introduce magnitude of market vector gains
                            # 
                            # if value from a [timeperiod] ago is <= [percentage] less than today
                            #   sell
                            # else
                            #   do nothing, the gain potential isnt that good
                            # 
                            # 
                            # )
                            sell = auth_client.sell()
                            logging.warning('{} - {}'.format(datetime.now(), sell)) 
                            print("Order status logged.")
                            cont = True
                        elif choice == "n":
                            print("Skipping sell order.")
                            cont = True
                        else:
                            ("Invalid input. Only 'y' or 'n' are allowed.")
        run()
        run = False
    
    # Wait until the next hour to run program again
    print("\nrun() completed. Sleeping until the top of the upcoming hour.\n")
    time.sleep((60*60) - datetime.now().minute*60 - (datetime.now().microsecond/1000000))
        