
class Wallet:

    def __init__(self):
        self.money = 100000
        self.coin = 0

    def addCoin(self, count):
        self.coin += count

    def addMoney(self, count):
        self.money += count

    def toString(self):
        return f"coin: {self.coin}, money: {self.money}"
