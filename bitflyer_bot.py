from orderbook import OrderBook
import requests
import json
import time
import sys
from datetime import datetime
from datetime import timedelta


class BitflyerBot:

    def __init__(self):
        self.ETH_JPY = "ETH_JPY"
        self.slack_token = "TAWSVC1TJ/B023EDHPMFW/N3VhuoXrRO30B6oghvpFL3SE"
        self.period = 0.5
        self.url = "https://api.bitflyer.com"
        self.path = "/v1/ticker"
        self.query = f"?product_code={self.ETH_JPY}"
        self.api = self.url + self.path + self.query
        self.buy_rate = 0.05 / 100
        self.sell_rate = 0.05 / 100
        self.buy_count = 0.05
        self.sell_count = 0.049
        self.order_book = OrderBook()
        

    def run(self):
        while True:
            resp = requests.get(self.api)
            obj = json.loads(resp.text)

            lastPrice = obj["ltp"]

            if "Idle" in self.order_book.order_state:
                self.order_book.BuyOrder(lastPrice * ( 1 - self.buy_rate), self.buy_count)
                print( f"ltp: {lastPrice}, details : {self.order_book.toString()}")

            elif "Purchased" in self.order_book.order_state:
                self.order_book.SellOrder(lastPrice * ( 1 + self.sell_rate), self.sell_count)
                print( f"ltp: {lastPrice}, details : {self.order_book.toString()}")
            else:
                self.order_book.Purchase(lastPrice)
            
            time.sleep(self.period)


if __name__ == "__main__":
    bot = BitflyerBot()
    bot.run()

