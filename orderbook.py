
from wallet import Wallet


class OrderBook:
    def __init__(self):
        self.wallet = Wallet()
        self.fee_rate = 0.03 / 100
    
    def Buy(self, price, count):
        self.wallet.addCoin( self.fee(count))
        self.wallet.addMoney( - (price * count))
        print(f"buy:: price: {price} count: {count} wallet: {self.wallet.toString()}")
        
        
    def Sell(self, price, count):
        self.wallet.addCoin(-count)
        self.wallet.addMoney(self.fee(price * count))
        print(f"sell:: price: {price} count: {count} wallet: {self.wallet.toString()}")

    def fee(self, item):
        return item - (item * self.fee_rate)
        
