from trail import SMATrail
import requests
import json
import time


class BitflyerBot:

    def __init__(self):
        self.ETH_JPY = "ETH_JPY"
        self.period = 1
        self.url = "https://api.bitflyer.com"
        self.path = "/v1/ticker"
        self.query = f"?product_code={self.ETH_JPY}"
        self.api = self.url + self.path + self.query

    def run(self):
        trail = SMATrail(1500)
        while True:
            resp = requests.get(self.api)
            obj = json.loads(resp.text)

            lastPrice = obj["ltp"]

            trail.Tracking(lastPrice)
            
            time.sleep(self.period)


if __name__ == "__main__":
    bot = BitflyerBot()
    bot.run()

