from datetime import datetime
import random
import time
import requests
from tqdm import tqdm
from helpers import HELPERS, Items, Platforms
from database import get_item, update_item
from item import Item

YUANTL = HELPERS.Buff.getCNY_TRY()
RETRY = 4
HEADERS = HELPERS.Buff.headers
PARAMS = HELPERS.Buff.params
PROXIES = None


def getBuffDataByItemID(itemid):
    PARAMS["goods_id"] = str(itemid)
    buffItemSellURL = HELPERS.Buff.LS_url
    buffItemBuyURL = HELPERS.Buff.HB_url

    for try_count in range(RETRY):
        try:
            sellResponseRequest = requests.get(buffItemSellURL, params=PARAMS, headers=HEADERS, proxies=PROXIES, timeout=5)
            sellResponse = sellResponseRequest.json()["data"]["items"]
            break
        except Exception as e:
            if sellResponseRequest.status_code == 429:
                time.sleep(random.randint(1,3))
            else:
                tqdm.write(f"[ERROR]\tBUFF163 Sell Response {e} \n\t --> Trying again...{try_count+2}")
            continue

    for try_count in range(RETRY):
        try:
            buyResponseRequest = requests.get(buffItemBuyURL, params=PARAMS, headers=HEADERS, proxies=PROXIES, timeout=5)
            buyResponse = buyResponseRequest.json()["data"]["items"]
            break
        except Exception as e:
            if buyResponseRequest.status_code == 429:
                time.sleep(random.randint(1,3))
            else:
                tqdm.write(f"[ERROR]\tBUFF163 Buy Response {e} \n\t --> Trying again...{try_count+2}")
            continue

    try:
        lowestSell = round(float(sellResponse[0].get("price"))*YUANTL, 2)
    except Exception:
        lowestSell = None
    try:
        highestBuy = round(float(buyResponse[0].get("price"))*YUANTL, 2)
    except Exception:
        highestBuy = None

    data = {
        "lowestSell" : lowestSell,
        "highestBuy" : highestBuy
    }
    return data

def requestBuffData(itemname:str):
    item:Item = get_item(name=itemname)
    buffid = item.getBuffID()
    buffPrices:dict = getBuffDataByItemID(buffid)
    buffurl = f"https://buff.163.com/goods/{buffid}?from=market#tab=selling"
    
    bufflowestsell = buffPrices.get("lowestSell")
    buffhighestbid = buffPrices.get("highestBuy")

    if item:
        item.setBuffData(data={
            Items.BUFF_ID:buffid,
            Items.PRICES.Buff_LS:bufflowestsell,
            Items.PRICES.Buff_HB:buffhighestbid,
            Items.URLS.Buff:buffurl,
            Items.UPDATE.Buff:datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        update_item(item=item, platform=Platforms.BUFF)
    else:
        tqdm.write(f"{itemname} is not found in the database.")
        return