import requests
import json
import time
import sys
from datetime import datetime
from datetime import timedelta

ETH_JPY = "ETH_JPY"
BTC_JPY = "BTC_JPY"

LAST_PRICE = "LP"
LAST_SELL = "LS"
LAST_BUY = "LB"
LAST_TOTAL_COUNT = "LTC"
LAST_ID = "LI"

last = {
    ETH_JPY : {
        LAST_PRICE : 0,
        LAST_SELL : 0,
        LAST_BUY  : 0,
        LAST_TOTAL_COUNT : 0,
        LAST_ID : 1000000000
    },
    BTC_JPY : {
        LAST_PRICE : 0,
        LAST_SELL : 0,
        LAST_BUY  : 0,
        LAST_TOTAL_COUNT : 0,
        LAST_ID : 1000000000,
    }
}

coin_name = {ETH_JPY: "ETH/JPY", BTC_JPY: "BTC/JPY"}
slack_token = "TAWSVC1TJ/B023EDHPMFW/N3VhuoXrRO30B6oghvpFL3SE"
period = 180
last_time = datetime.utcnow() + timedelta(seconds=-period)

def getDelta(coin_pair, type, value):
    delta = value -last[coin_pair][type]
    last[coin_pair][type] = value
    return delta

def getTotalStock(items):
    item = list()
    for arr in items:
        item.append(arr["size"])
    return round(sum(item))


def getDeltaRate(cur, last):
    if cur == 0 or last == 0:
        return 0
    return round(((cur / last) - 1) * 100, ndigits=3)


def getVolume(coin_pair):
    # GET /v1/executions'?product_code=ETH_JPY&count=100&after=500';
    """
    {
        "id": 2221228246,
        "side": "BUY",
        "price": 282902,
        "size": 0.01,
        "exec_date": "2021-05-31T12:09:52.83",
        "buy_child_order_acceptance_id": "JRF20210531-120952-366775",
        "sell_child_order_acceptance_id": "JRF20210531-120952-314907"
    },
    """
    count = 500
    url = f"https://api.bitflyer.com/v1/executions?product_code={coin_pair}&count={count}&after={last[coin_pair][LAST_ID]}"
    resp = requests.get(url)
    resp_json = json.loads(resp.text)

    volume = { "total_count" : 0 , "total_buy" :0, "total_sell" : 0 , "delta_count" : 0, "delta_buy" :0 , "delta_sell" : 0}

    for item in resp_json:
        time = item["exec_date"].split('.')[0]
        item_date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        if item_date < last_time:
            break

        last[coin_pair][LAST_ID] = item["id"]
        volume["total_count"] += 1
        if "BUY" in item["side"]:
            volume["total_buy"] += item["size"]
        else:
            volume["total_sell"] += item["size"]

    volume["delta_count"] = getDelta(coin_pair, LAST_TOTAL_COUNT, volume["total_count"])
    volume["delta_buy"] = round(getDelta(coin_pair, LAST_BUY, volume["total_buy"]) , ndigits=2)
    volume["delta_sell"] = round(getDelta(coin_pair, LAST_SELL, volume["total_sell"]), ndigits=2)

    volume['total_buy'] = round(volume['total_buy'], ndigits=2)
    volume['total_sell'] = round(volume['total_sell'], ndigits=2)

    return volume


def getCoinInfo(coin_pair):
    url = f"https://api.bitflyer.com/v1/board?product_code={coin_pair}"
    resp = requests.get(url)
    resp_json = json.loads(resp.text)

    current = resp_json["mid_price"]
    delta_rate = getDeltaRate(current, last[coin_pair][LAST_PRICE])
    delta = getDelta(coin_pair , LAST_PRICE, current)
    
    bids = getTotalStock(resp_json["bids"])
    asks = getTotalStock(resp_json["asks"])

    volume = getVolume(coin_pair)

    return { 
        "name": coin_name[coin_pair],
        "price": current,
        "last_price": last[coin_pair][LAST_PRICE],
        "asks": asks,
        "bids": bids,
        "delta": delta,
        "delta_rate": delta_rate,
        "total_count" : volume["total_count"],
        "delta_count" : volume["delta_count"],
        "total_buy" : volume["total_buy"],
        "delta_buy" : volume["delta_buy"],
        "total_sell" : volume["total_sell"],
        "delta_sell" : volume["delta_sell"]
    }


def postSlack(text):
    headers = {
        'Content-type': 'application/json',
    }
    data = {
        'text': text
    }
    json_str = json.dumps(data)
    post_url = f"https://hooks.slack.com/services/{slack_token}"
    resp = requests.post(post_url, data=json_str, headers=headers)
    print("post status :", resp.text)


def makeText(info):
    return f"""
{info['name']} : {info['price']} ({info['delta']}) 
가격변동률 : {info['delta_rate']}%
거래량: {info['total_count']}건 ({info['delta_count']})
매수량 : {info['total_buy']}개 ({info['delta_buy']})
매도량 : {info['total_sell']}개 ({info['delta_sell']})
Asks ({info['asks']}) / Bids ({info['bids']})"""


def run():
    while True:
        eth_info = getCoinInfo(ETH_JPY)
        # btc_info = getCoinInfo(BTC_JPY)

        now = datetime.now()
        text = f"""
{makeText(eth_info)}
--------------{now.strftime("%m/%d %H:%M")}--------------

"""
        postSlack(text)
        time.sleep(period)


if __name__ == "__main__":
    run()

