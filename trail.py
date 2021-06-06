import json
import requests

class OrderBook:
    def __init__(self):
        self.fee_rate = 0.03 / 100
        self.money = 100000
        self.coin = 0

    def Buy(self, price, count):
        self.coin += self.fee(count)
        self.money -= (price * count)

    def Sell(self, price, count):
        self.coin -= count
        self.money += self.fee(price * count)

    def fee(self, item):
        return item - (item * self.fee_rate)


class SMATrail:
    def __init__(self, initial_boundary):
        self.initial_price = 0
        self.state = ""
        self.boundary = initial_boundary
        self.order_book = OrderBook()
        self.price_set = set()
        self.average_price = 0
        self.slack_token = "TAWSVC1TJ/B023EDHPMFW/N3VhuoXrRO30B6oghvpFL3SE"

    def BuyOrder(self, price, boundary):
        """
        매수 트레일링 시작
        """
        if self.state != "":
            return

        self.boundary = boundary
        self.initial_price = price + self.boundary
        self.state = "BUY"

    def SellOrder(self, price, boundary):
        """
        매도 트레일링 시작
        """
        if self.state != "WAIT":
            return

        self.boundary = boundary
        self.initial_price = price - self.boundary
        self.state = "SELL"

    def Buy(self, price):
        """
        매수
        """
        count = self.order_book.money / price; # 풀매수
        self.order_book.Buy(price, count)
        self.Report(price)
        self.state = "WAIT"

    def Sell(self, price):
        """
        매도
        """
        self.order_book.Sell(price, self.order_book.coin) # 풀매도
        self.Report(price) 
        self.state = ""

    def Tracking(self, price):
        """
        가격을 트래킹해서 매매시점 파악 및 매매를 진행
        """
        self.ValidatePrice(price)

        if "BUY" in self.state:
            if self.initial_price > price + self.boundary:
                self.initial_price = price + self.boundary
            elif self.initial_price <= price:
                self.Buy(price)
        if "SELL" in self.state:
            if self.initial_price < price - self.boundary:
                self.initial_price = price - self.boundary
            elif self.initial_price >= price:
                self.Sell(price)

    def ValidatePrice(self, price):
        """
        가격 검증을 통해 매매시점을 파악, 매매주문 입력
        """
        self.SMA(price)  # sma는 트레일링과 상관없이 진행

        if self.average_price == 0:
            return

        if self.average_price + self.boundary < price:
            self.SellOrder(price, 1000)
        elif self.average_price - self.boundary > price:
            self.BuyOrder(price, 1500)

    def SMA(self, price):
        """
        이동평균계산
        """
        self.price_set.add(price)
        self.average_price = sum(self.price_set) / len(self.price_set)

        if len(self.price_set) > 1000:
            self.price_set.pop()


    def Report(self, order_price):
        """
        매매결과 레포트 
        """
        text = f"{self.state} - 잔고 : ({self.order_book.money}엔, {self.order_book.coin}개), 매매금액 : {order_price}"
        self.postSlack(text)


    def postSlack(self, text):
        
        headers = {
            'Content-type': 'application/json',
        }
        data = {
            'text': text
        }

        json_str = json.dumps(data)
        post_url = f"https://hooks.slack.com/services/{self.slack_token}"
        requests.post(post_url, data=json_str, headers=headers)
