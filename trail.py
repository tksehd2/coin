import math
from orderbook import OrderBook
import time
class Trail:
    def __init__(self) :
        self.initial_price = 0
        self.state = ''
        self.boundary = 0
        self.order_book = OrderBook()

    def BuyOrder(self, price, boundary):
        self.boundary = boundary
        self.initial_price = price + self.boundary
        self.state = "BUY"

    def SellOrder(self, price, boundary):
        self.boundary = boundary
        self.initial_price = price - self.boundary
        self.state = "SELL"

    def Tracking(self, price):
        if "BUY" in self.state:
            if self.initial_price > price + self.boundary:
                self.initial_price = price + self.boundary
                print( f'tracking {self.state} targetPrice: {self.initial_price} cur: {price}')
            elif self.initial_price <= price:
                self.order_book.Buy(price , 0.05)
                self.SellOrder(price , self.boundary)

        if "SELL" in self.state:
            if self.initial_price < price - self.boundary:
                self.initial_price = price - self.boundary
                print( f'tracking {self.state} targetPrice: {self.initial_price} cur: {price}')
            elif self.initial_price >= price: 
                self.order_book.Sell(price , self.order_book.wallet.coin)
                self.BuyOrder(price , self.boundary)