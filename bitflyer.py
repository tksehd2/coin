import requests
import json
import time
import sys
from datetime import datetime

ETH_JPY = "ETH_JPY"
BTC_JPY = "BTC_JPY"

last_price = {ETH_JPY: 0, BTC_JPY: 0}
coin_name = {ETH_JPY: "ETH/JPY", BTC_JPY: "BTC/JPY"}

period = 180

def getTotalStock(items):
    item = list()
    for arr in items:
        item.append(arr["size"])
    return round(sum(item))


def getDeltaRate(cur, last):
    if cur == 0 or last == 0:
        return 0
    return round(((cur / last) - 1) * 100, ndigits=3)


def getCoinInfo(coin_pair):
    url = f"https://api.bitflyer.com/v1/board?product_code={coin_pair}"
    resp = requests.get(url)
    resp_json = json.loads(resp.text)

    last = last_price[coin_pair]
    current = resp_json["mid_price"]
    delta = current - last
    delta_rate = getDeltaRate(current, last)

    last_price[coin_pair] = current

    bids = getTotalStock(resp_json["bids"])
    asks = getTotalStock(resp_json["asks"])
    return {"name": coin_name[coin_pair], "price": current, "last_price" : last, "asks": asks, "bids": bids, "delta": delta, "delta_rate" : delta_rate}


def postSlack(text):
    headers = {
        'Content-type': 'application/json',
    }
    data = {
        'text': text
    }
    json_str = json.dumps(data)
    post_url = "https://hooks.slack.com/services/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"
    resp = requests.post(post_url, data=json_str, headers=headers)
    print("post status :", resp.text)


def makeText(info):    
    return f"""
{info['name']} : {info['price']}({info['delta']}) 
가격변동률 : {info['delta_rate']}%
Asks : {info['asks']}
Bids : {info['bids']}"""    


def run():
    while True:
        eth_info = getCoinInfo(ETH_JPY)
        btc_info = getCoinInfo(BTC_JPY)

        now = datetime.now()
        text = f"""
{makeText(eth_info)}
{makeText(btc_info)}
--------------{now.strftime("%m/%d %H:%M")}--------------

"""    
        postSlack(text)
        time.sleep(period)     

if __name__ == "__main__":
    run()

