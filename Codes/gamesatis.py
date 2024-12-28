from datetime import datetime, timedelta
from driver import Driver
from helpers import HELPERS, Items, Platforms
import time
from tqdm import tqdm
from selenium.webdriver.common.by import By
from item import Item
from database import get_item, update_item
from buff import requestBuffData

class GameSatis():
    def __init__(self):
        self.cookies = HELPERS.GameSatis.cookies
        self.headers = HELPERS.GameSatis.headers
        self.driverObj = Driver()
        self.driver = self.driverObj.get_chrome_driver()
        
    def updateItems(self) -> None:
        self.driverObj.goTo("https://www.gamesatis.com/cs2-skin?category=cs2-skin&order=fiyat-azalan&q=&page=1")
        #self.driverObj.set_cookies(cookie_list=self.cookies)
        try:
            pages = self.driver.find_elements(By.XPATH, "//ul[@class='paginate']/li")
            pagenum = int(pages[-2].text)
        except Exception:
            pagenum = 100

        for p in tqdm(range(pagenum)):
            self.driverObj.goTo(f"https://www.gamesatis.com/cs2-skin?category=cs2-skin&order=fiyat-azalan&q=&page={p+1}")
            time.sleep(2)
            items_frontend = self.driver.find_elements(By.XPATH, "//a[@class='product product-skin']")
            diction = HELPERS.GameSatis.exterior_dict
            for itemf in items_frontend:
                try:
                    skin:str = itemf.find_element(By.XPATH, "./h3").text.strip()
                    skin = skin.replace("StatTrak", "StatTrak™") if "StatTrak" in skin else skin
                    exterior = itemf.find_element(By.XPATH, "./label").text.strip()
                    name = f"{skin} ({diction.get(exterior)})" if exterior in diction else skin
                except Exception:
                    tqdm.write(f"[ERROR] {skin}\tName cannot be scraped.")
                    continue
                try:
                    price_text = itemf.find_element(By.XPATH, "./div[@class='selling-price']").text.strip()
                    cleaned_number = price_text.replace('.', '').replace(',', '.').replace('₺', '').strip()
                    price = float(cleaned_number)
                except Exception:
                    tqdm.write(f"[ERROR] {skin}\tPrice tag cannot be scraped.")
                    continue
                try:
                    url = itemf.get_attribute('href')
                except Exception:
                    tqdm.write(f"[ERROR] {skin}\tURL is not found.")
                    url = "https://www.gamesatis.com/cs2-skin"
                try:
                    image = itemf.find_element(By.XPATH, ".//img").get_attribute('src')
                except Exception:
                    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNNLEL-qmmLeFR1nxJuepFOgPYfnwHR56vcw&s"
                try:
                    floatVal = itemf.find_element(By.XPATH, "./div[@class='float-rank']").text.replace('Float: ', '').strip()
                    floatVal = float(floatVal)
                except Exception:
                    tqdm.write(f"[ERROR] {skin}\tNo Float value available.")
                    floatVal = None

                item:Item = get_item(name=name)
                if item:
                    lastbuffupdate = datetime.strptime(item.getBuffLastUpdate(), "%Y-%m-%d %H:%M:%S") if item.getBuffLastUpdate() else None
                    if not item.getBuffLS() or not lastbuffupdate or lastbuffupdate < datetime.now() - timedelta(days=1):
                        requestBuffData(itemname=name)
                        item:Item = get_item(name=name)
                    item.setGamesatisData(data={
                        Items.PRICES.Gamesatis : price,
                        Items.URLS.Image : image,
                        Items.URLS.Gamesatis : url,
                        Items.FLOATS.Gamesatis : floatVal,
                        Items.UPDATE.Gamesatis : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    update_item(item=item, platform=Platforms.GAMESATIS)
                else:
                    tqdm.write(f"[ERROR] {name} is not found in the database.")
                    continue