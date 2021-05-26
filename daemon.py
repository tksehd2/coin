import requests
import json
import time
import sys

last_price = {"ethjpy": 0, "btcjpy": 0}
# curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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
slack_post_url = "https://hooks.slack.com/services/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"
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


def postSlack(post_url, text):
    headers = {
        'Content-type': 'application/json',
    }
    data = {
        'text': text
    }
    json_str = json.dumps(data)
    resp = requests.post(post_url, data=json_str, headers=headers)
    print("post status :", resp.text)


def getCoinInfo(market, coin):
    price_url = f"https://api.cryptowat.ch/markets/{market}/{coin}/price"
    order_url = f"https://api.cryptowat.ch/markets/{market}/{coin}/orderbook"

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


def run(post_url):
    # market = "bitflyer"
    # coin = "ethjpy"
    while(True):
        eth_info = getCoinInfo('bitflyer', 'ethjpy')
        btc_info = getCoinInfo('bitflyer', 'btcjpy')

        text = f"""
ETH/JPY : {eth_info['price']}({eth_info['delta']}) 
가격변동률 : rate({getDeltaRate(eth_info['price'] , eth_info['last_price'])}%)
ASK : {eth_info['ask']}
BID : {eth_info['bid']}

BTC/JPY : {btc_info['price']}({btc_info['delta']}) 
가격변동률 : rate({getDeltaRate(btc_info['price'] , btc_info['last_price'])}%)
ASK : {btc_info['ask']}
BID : {btc_info['bid']}
---------------------------
        """

        postSlack(post_url, text)
        time.sleep(period)


if __name__ == "__main__":
    url = sys.argv[1]
    print(url)
    run(url)

