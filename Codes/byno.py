from datetime import datetime, timedelta
from tqdm import tqdm
from item import Item
from helpers import HELPERS, Items, CONSTANTS, Platforms
from database import update_item, get_item
import requests
import html
import pickle
import os
from buff import requestBuffData

class ByNoGame():
    def getLatestItems(self):
        if not os.path.exists(HELPERS.Bynogame.PROCESSED_ITEMS_PATH):
            with open(HELPERS.Bynogame.PROCESSED_ITEMS_PATH, 'wb') as f:
                pickle.dump(set(), f)
                processed_items = set()
        else:
            with open(HELPERS.Bynogame.PROCESSED_ITEMS_PATH, 'rb') as f:
                processed_items = pickle.load(f)

        item_limit = HELPERS.Bynogame.pickled_item_limit
        if len(processed_items) >= item_limit:
            sorted_items = sorted(processed_items)
            oldest = sorted_items[:item_limit//2]
            processed_items.difference_update(oldest)

        params = {'page': '0', 'limit': f'{CONSTANTS.item_count}'}
        response = requests.get(HELPERS.Bynogame.bynogame_latestitems_url, params=params)
        items:list[dict] = response.json()["payload"]
        for bynoitem in tqdm(reversed(items), total=len(items)):
            processID = bynoitem.get("processId", 0)
            label = bynoitem.get("label", None)
            isBynoSeller = bynoitem.get("autoDelivery")
            if processID not in processed_items and label != "sold" and not isBynoSeller:
            #if True:  #debugging
                itemname:str = bynoitem["name"]
                itemname = html.unescape(itemname)
                itemname = itemname.replace("’", "'")
                itemname = itemname.replace("Kiss?Love", "Kiss♥Love")
                item:Item = get_item(name=itemname)

                if item:
                    lastbuffupdate = datetime.strptime(item.getBuffLastUpdate(), "%Y-%m-%d %H:%M:%S") if item.getBuffLastUpdate() else None
                    if not item.getBuffLS() or not lastbuffupdate or lastbuffupdate < datetime.now() - timedelta(days=1):
                        requestBuffData(itemname=itemname)
                        item:Item = get_item(name=itemname)
                    item.setBynoGameData(data={
                        Items.PRICES.BynoGame:bynoitem["price"],
                        Items.URLS.BynoGame:f"https://www.bynogame.com/tr/oyunlar/cs2-skin/{bynoitem['slug']}",
                        Items.URLS.Image:bynoitem["image"],
                        Items.FLOATS.BynoGame:bynoitem.get("info", None).get("float", None),
                        Items.UPDATE.BynoGame:datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    update_item(item=item, platform=Platforms.BYNOGAME)
                else:
                    tqdm.write(f"[ERROR]{itemname} is not found in the database.")
                    continue

                processed_items.add(processID)

        with open(HELPERS.Bynogame.PROCESSED_ITEMS_PATH, 'wb') as f:
            pickle.dump(processed_items, f)
        