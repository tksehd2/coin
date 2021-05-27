import requests
import json
import time
import sys

last_price = {"ethjpy": 0, "btcjpy": 0}
slack_token = "TAWSVC1TJ/B023EDHPMFW/N3VhuoXrRO30B6oghvpFL3SE"
api_key = "02213GI7UV4W05LZC2PN"
period = 180

def getTotalStock(items):
    item = list()
    for arr in items:
        item.append(arr[1])
    return round(sum(item))


def getDeltaRate(cur, last):
    if cur == 0 or last == 0:
        return 0

    return round(((cur / last) - 1) * 100, ndigits=3)


def postSlack(text):
    headers = {
        'Content-type': 'application/json',
    }
    data = {
        'text': text
    }
    post_url = f"https://hooks.slack.com/services/{slack_token}"
    json_str = json.dumps(data)
    resp = requests.post(post_url, data=json_str, headers=headers)
    print("post status :", resp.text)


def getCoinInfo(market, coin):
    price_url = f"https://api.cryptowat.ch/markets/{market}/{coin}/price?apikey={api_key}"
    order_url = f"https://api.cryptowat.ch/markets/{market}/{coin}/orderbook?apikey={api_key}"

    price_resp = requests.get(price_url)
    order_resp = requests.get(order_url)

    price_json = json.loads(price_resp.text)["result"]
    order_json = json.loads(order_resp.text)["result"]

    asks = order_json["asks"]
    bids = order_json["bids"]

    asks_total = getTotalStock(asks)
    bids_total = getTotalStock(bids)
    current = price_json["price"]
    last = last_price[coin]
    delta = current - last
    last_price[coin] = current

    return {"price": current, "last_price" : last, "ask": asks_total, "bid": bids_total, "delta": delta}


def run():
    # market = "bitflyer"
    # coin = "ethjpy"
    while(True):
        eth_info = getCoinInfo('bitflyer', 'ethjpy')
        btc_info = getCoinInfo('bitflyer', 'btcjpy')

        text = f"""
ETH/JPY : {eth_info['price']}({eth_info['delta']}) 
가격변동률 : {getDeltaRate(eth_info['price'] , eth_info['last_price'])}%
ASK : {eth_info['ask']}
BID : {eth_info['bid']}

BTC/JPY : {btc_info['price']}({btc_info['delta']}) 
가격변동률 : {getDeltaRate(btc_info['price'] , btc_info['last_price'])}%
ASK : {btc_info['ask']}
BID : {btc_info['bid']}
---------------------------
        """

        postSlack( text)
        time.sleep(period)


if __name__ == "__main__":
    run()

