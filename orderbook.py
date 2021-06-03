
from wallet import Wallet


class OrderBook:
    def __init__(self):
        self.wallet = Wallet()
        self.order_state = "Idle"
        self.order_price = 0
        self.order_count = 0
        self.fee_rate = 0.03 / 100
    
    def BuyOrder(self, price, count):
        self.order_state = "BuyOrder"
        self.order_price = price
        self.order_count = count
        
        
    def SellOrder(self, price, count):
        self.order_state = "SellOrder"
        self.order_price = price
        self.order_count = count
        
    def Purchase(self, ltp):

        if "Buy" in self.order_state:
            if ltp > self.order_price:
                return
            elif ltp < self.order_count:
                self.order_state = "Purchased"
                self.wallet.addCoin( self.order_count - ( self.order_count * self.fee_rate))
                self.wallet.addMoney( - (ltp * self.order_count))
                print( f"ltp: {ltp}, details : {self.toString()}")
            else:
                self.order_state = "Purchased"
                self.wallet.addCoin(self.order_count - ( self.order_count * self.fee_rate))
                self.wallet.addMoney( -(self.order_price * self.order_count))
                print( f"ltp: {ltp}, details : {self.toString()}")
        
        if "Sell" in self.order_state:
            if ltp < self.order_price:
                return
            elif ltp > self.order_price:
                self.order_state = "Idle"
                self.wallet.addCoin( -self.order_count)
                self.wallet.addMoney ( self.order_price * self.order_count - (self.order_price * self.order_count * self.fee_rate))
                print( f"ltp: {ltp}, details : {self.toString()}")
            else:
                self.order_state = "Idle"
                self.wallet.addCoin(-self.order_count)
                self.wallet.addMoney( ltp * self.order_count - (ltp * self.order_count* self.fee_rate))
                print( f"ltp: {ltp}, details : {self.toString()}")
                
    def toString(self):
        return f"state: {self.order_state} price: {self.order_price} count: {self.order_count} wallet: {self.wallet.toString()}"
        
