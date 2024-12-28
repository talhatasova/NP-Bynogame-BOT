from datetime import datetime
from enum import Enum
import requests

class Platforms():
    BYNOGAME = "ByNoGame"
    GAMESATIS = "GameSatis"
    BUFF = "Buff"
    
class Items:
    NAME = "name"
    BUFF_ID = "id"
    class FLOATS:
        BynoGame = "float"
        Gamesatis = "float"
    class PRICES:
        Buff_LS = "price_ls"
        Buff_HB = "price_hb"
        BynoGame = "price"
        Gamesatis = "price"
    class RATES:
        BynoGame_LS = "ls_rate"
        BynoGame_HB = "hb_rate"
        Gamesatis_LS = "ls_rate"
        Gamesatis_HB = "hb_rate"
    class URLS:
        Buff = "url"
        BynoGame = "url"
        Gamesatis = "url"
        Image = "image"
    class UPDATE:
        Buff = "last_update"
        BynoGame = "last_update"
        Gamesatis = "last_update"

class HELPERS:
    PROXY_PICKLE_PATH = 'running_proxies.pkl'
    
    class Buff:
        item_id_path = r"C:\Users\tasov\OneDrive\Desktop\Projects\Upwork Projects\ByNo-Discord-BOT\env\Settings\json Files\cs2_marketplaceids.json"
        LS_url = "https://buff.163.com/api/market/goods/sell_order"
        HB_url = "https://buff.163.com/api/market/goods/buy_order"
        try_count = 1

        headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-GB,en;q=0.9,tr-TR;q=0.8,tr;q=0.7,en-US;q=0.6',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
        }

        params = {
                'game': 'csgo',
                #'page_num': '1',
                #'sort_by': 'price.asc',
            }
        
        @classmethod
        def getCNY_TRY(cls) -> float:
            path = r"Settings/txt Files/currency.txt"
            with open(path, "r") as f:
                rate, date = f.readline().split(",")
            
            dt_object = datetime.strptime(date, "%d/%m/%Y")
            if dt_object < datetime.now():
                try:
                    url = "https://api.exchangerate-api.com/v4/latest/CNY"
                    response = requests.get(url)
                    data = response.json()
                    rate = float(data["rates"]["TRY"])
                    with open(path, "w") as f:
                        formatted_date = datetime.now().strftime("%d/%m/%Y")
                        f.write(f"{str(rate)},{formatted_date}")
                except:
                    pass
            return rate


    class Bynogame:
        pickled_item_limit = 1000
        PROCESSED_ITEMS_PATH = 'latest_items.pkl'
        bynogame_latestitems_url = "https://listing.bynogame.net/api/listings/cs2"
        logo_url = "https://cdn.bynogame.com/logo/bng-black-logo-1699353125086.png"
        cookies = {
            'bynogamecom': 'bynogamecom254.56.2.31-20240121165640_19563',
            '_ym_uid': '1706708815398371937',
            'FPID': 'FPID2.2.WuGfNqa3xE6V%2F6mXmFnlQeZrrXKv63yhdKRDoDBQwGA%3D.1719165091',
            '_acceptCookies': '[{"updatedAt":1719165101015,"categories":{"essential":true,"analytical":true,"marketing":true}}]',
            '_fbp': 'fb.1.1719847267945.1908883469',
            '_ym_d': '1722637400',
            '_gcl_au': '1.1.949851429.1728247057',
            '_clck': 'llskay%7C2%7Cfps%7C0%7C1740',
            'PHPSESSID': '4id0cm4de734h7lg801hu7l5sm',
            '_gtmeec': 'eyJlbSI6ImI2MjYwYzM3NjExNmVlY2ZiYjE3ZmQ3NTM1ZmY3ODE4MWMwNDYxMDEyM2Y2NDgwZjZkZTZmZjljZWI4NjQ2MTYiLCJwaCI6IjZlODRlNGQ2ODdlMzk4Y2MyZDM3YzQ0MWI2NWUzNGM3MTE0OGVmYzFjYzFiOTg4MDY1YzI0OTA2ODVhYmFlOWEiLCJleHRlcm5hbF9pZCI6Ild1R2ZOcWEzeEU2Vi82bVhtRm5sUWVacnJYS3Y2M3loZEtSRG9EQlF3R0E9LjE3MTkxNjUwOTEifQ%3D%3D',
            '_gid': 'GA1.2.296266924.1730920904',
            '_ym_isad': '1',
            'FPLC': 'a8OIg4GRxJgjLFoKkgK7mnpZmbqg0G0Hka%2B9G3zZOQKRf0huD5DHSPiuTa62APspDTptgsNwaetD6kTo6RxIm3c0xY3jxM%2FBy9D8j9JXdyrdiQuthxpil4Kf5JdB%2FA%3D%3D',
            '__cf_bm': 'Mv.IjflrsxU9YY5Rh9Z4mrxhk0oP0E_jUKhC4GMgfm4-1730932055-1.0.1.1-fIYLC1VoHPthJ6UuYqGc9bVrKUJSqDThhFEXddzbkNJk62YfM17EslFjic9nCI.ncrqXerX9j1V5dbG00orPVQ',
            'cf_clearance': 'uDPVsQIEt.d0lpFzBA29jVF3EWHPJglbLyyqzeFWWog-1730932056-1.2.1.1-npBT3cZeuRCdcXOF31ScZgetI2QokGVIOKV0aQE9mNQqzJlHQ54ZytnRq62AgFa4xcbRChZaIraAoe3zParQQybEQi6TINJY6RnfbCbNgOuaKhIYrIKpjbQv2Vy7Bs9mA4Sct2XSp1JDXAKYRf7VhymT7xA6gbpsYd5o5l6Fk8xXf9BhYmUl8WwfvH0J1PpXb39vFGuAh_4TyHCZVGpCRgJxelCcs78inl_LlrBGjfks8LJm84Sl3w0KIFqcYkGxbv9vUuDn1Fzcl20jSxOdJz5SWlU9uUeXJxIafgQ3Jf45O85gP3xKn1VNzsz4nAUjBFT2U_HbHrd_Yj1iH4JtHedUlr0aGaCkKzYG0NzPGXpIUcA8lUrosL7Hn5XSpvPR',
            '_gat_gtag_UA_34048142_1': '1',
            'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA2ODE4MywidXNlcklkIjoxMDY4MTgzLCJlbWFpbCI6InRhc292YTk0MEBnbWFpbC5jb20iLCJhdmF0YXIiOiJodHRwczpcL1wvbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbVwvYVwvQUNnOG9jSmJJVEpaSHkyaHFESDlvWWk0UGxxWk1yZUNKdWZsZ0JvclJJWVgzNk9YclZMdVVsTTQ9czk2LWMiLCJwaG9uZSI6IjkwNTMxNzMzNzcwOSIsImxhbmciOiJUUiIsImJhbGFuY2UiOjQwMzYuMzUsImV4cCI6MTczMTUzNzA4MiwianRpIjoiMTczMDkzMjI4MjY3MmJlZTNhNTA1ZjIiLCJpYXQiOjE3MzA5MzIyODJ9.596tkXZJoa1B3X6TTQYkBHqFB9R_AWgq52ImT02wNuA',
            '_ga_JBRCYXTSG7': 'GS1.1.1730932051.55.1.1730932283.48.0.1160448961',
            '_ga': 'GA1.1.1077745010.1719165091',
            '_rdt_uuid': '1728247056756.222c8029-2a71-4eea-b36d-7c938e5cd0e8',
            '_ga_D6GM37LZ13': 'GS1.1.1730932051.4.1.1730932285.0.0.2064633856',
            '_ga_8BRJ8V0903': 'GS1.1.1730932051.4.1.1730932285.0.0.0',
        }
    

    class GameSatis:
        cookies = {
            'cf_clearance': 'JefgxNqbc1yfAAUCvk3gRESfRdJGrO0dMpFdVADP9.g-1724801927-1.2.1.1-1UTJCYNTrov3c8YZshmQdnuIrg5mLT0l_qqtyW.wXT0CpZr22XKX2rYM1GLBaeoeah8FE8TQEmJCQa1Jc7IueWMtJrgLI6cYLN3C8SgcZhlu0aevZXplCl1pI726ob64VCyaoS9LTf8FcCoJIsNWOKNS68pWBedM3B46PFMKKf6P.T9IezL43cdUoDk.MV.itoOL8y8kGsxoMd3BreMVQNkAsIju7pGdoCZ1F6l0KLGZgzBCxK7Etoy3WsodrHolimVAbw.6472hR66sbKO_CuhqjR6aY_Ph8DfqXL0dG8v9wQ2aKOzm2cZDDisAaBx7GLqMU1sFgAC8XJzgB3iQTiZ8NYew5agXn2S8q0Jg9hEt.OLpRNau3H3NML.glHzF5giOv5w8qr9wksTIlO8bTcm1ZL5LEbzoD_wm_dLnefadDT1LO50dWyamJtB3JgZC',
            '_gcl_au': '1.1.56028383.1730236505',
            '_gid': 'GA1.2.1781311950.1732193274',
            'ChatCount': '0',
            'chat_id': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6IklrRjZXbGR6WnpoNFMyRlZkREpvYzI5NU4wUmpZVGhSSWc9PSIsImV4cCI6bnVsbCwicHVyIjoiY29va2llLmNoYXRfaWQifX0%3D--40d856cf72b779cb128421286611ff109ce0731a',
            'trust_machine': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6Ik56SXdNamMxIiwiZXhwIjoiMjAyNC0xMi0yMlQxOToyNDo1OC44MjhaIiwicHVyIjoiY29va2llLnRydXN0X21hY2hpbmUifX0%3D--cb4324683b1673c379a70916047e45d458abb274',
            '_gs_session': 'e32329353d1f2e87f93bff151195ecaa',
            '_gat_UA-5495736-1': '1',
            '_ga_6FJF9CDBP6': 'GS1.1.1732314075.17.0.1732314075.60.0.0',
            '_ga': 'GA1.1.745350969.1730236505',
        }

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en;q=0.9,tr-TR;q=0.8,tr;q=0.7,zh-CN;q=0.6,zh;q=0.5,en-US;q=0.4',
            'cache-control': 'max-age=0',
            # 'cookie': 'cf_clearance=JefgxNqbc1yfAAUCvk3gRESfRdJGrO0dMpFdVADP9.g-1724801927-1.2.1.1-1UTJCYNTrov3c8YZshmQdnuIrg5mLT0l_qqtyW.wXT0CpZr22XKX2rYM1GLBaeoeah8FE8TQEmJCQa1Jc7IueWMtJrgLI6cYLN3C8SgcZhlu0aevZXplCl1pI726ob64VCyaoS9LTf8FcCoJIsNWOKNS68pWBedM3B46PFMKKf6P.T9IezL43cdUoDk.MV.itoOL8y8kGsxoMd3BreMVQNkAsIju7pGdoCZ1F6l0KLGZgzBCxK7Etoy3WsodrHolimVAbw.6472hR66sbKO_CuhqjR6aY_Ph8DfqXL0dG8v9wQ2aKOzm2cZDDisAaBx7GLqMU1sFgAC8XJzgB3iQTiZ8NYew5agXn2S8q0Jg9hEt.OLpRNau3H3NML.glHzF5giOv5w8qr9wksTIlO8bTcm1ZL5LEbzoD_wm_dLnefadDT1LO50dWyamJtB3JgZC; _gcl_au=1.1.56028383.1730236505; _gid=GA1.2.1781311950.1732193274; ChatCount=0; chat_id=eyJfcmFpbHMiOnsibWVzc2FnZSI6IklrRjZXbGR6WnpoNFMyRlZkREpvYzI5NU4wUmpZVGhSSWc9PSIsImV4cCI6bnVsbCwicHVyIjoiY29va2llLmNoYXRfaWQifX0%3D--40d856cf72b779cb128421286611ff109ce0731a; trust_machine=eyJfcmFpbHMiOnsibWVzc2FnZSI6Ik56SXdNamMxIiwiZXhwIjoiMjAyNC0xMi0yMlQxOToyNDo1OC44MjhaIiwicHVyIjoiY29va2llLnRydXN0X21hY2hpbmUifX0%3D--cb4324683b1673c379a70916047e45d458abb274; _gs_session=e32329353d1f2e87f93bff151195ecaa; _gat_UA-5495736-1=1; _ga_6FJF9CDBP6=GS1.1.1732314075.17.0.1732314075.60.0.0; _ga=GA1.1.745350969.1730236505',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"131.0.6778.86"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.86", "Chromium";v="131.0.6778.86", "Not_A Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        exterior_dict = {"StatTrak":"StatTrak™",
                         "Factory New":"Factory New",
                         "Minimal Wear":"Minimal Wear",
                         "Field Tested":"Field-Tested",
                         "Well Worn":"Well-Worn",
                         "Battle Scarred":"Battle-Scarred"}
class CONSTANTS:
    update_interval_seconds = 60
    item_count = 30
    thread_count = 1

    class THRESHOLDS:
        lowestSellRate = 100
        minprice = 150
        