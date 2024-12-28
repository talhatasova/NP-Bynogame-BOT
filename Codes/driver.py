from selenium_driverless.sync import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import os
import math
from item import Item
from helpers import HELPERS

class Driver():
    def __init__(self) -> None:
        self.driver = self.set_chrome_driver()
        pass

    def get_chrome_driver(self) -> webdriver.Chrome:
        if self.driver:
            return self.driver
        else:
            raise Exception("Driver is not properly set up!")
    
    def set_cookies(self, cookie_list:dict[str, str]):
        cookie_list = [{'name': name, 'value': value} for name, value in cookie_list.items()]
        for cookie in cookie_list:
            try:
                self.driver.add_cookie(cookie)
            except Exception as e:
                print(f"Error adding cookie {cookie['name']}: {e}")
        self.driver.refresh()

    def set_chrome_driver(self):
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values.cookies": 1,   # Allow cookies to be saved
            "profile.default_content_setting_values.notifications": 2,  # Block notifications
            "profile.default_content_setting_values.popups": 2      # Block popups
        }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--disable-search-engine-choice-screen")
        options.add_argument("--disable-save-password-bubble")
        #options.add_argument("--headless") #comment this line to see the crawling process

        driver = webdriver.Chrome(options=options)
        #driver.wait_for_cdp("Page.domContentEventFired", timeout=15)
        return driver
        
    def goTo(self, url:str):
        self.driver.get(url=url)

    def buyAnItem(self, item:Item, counterOffer:bool=False):
        self.goTo(url=item.getBynoURL())
        self.set_cookies()
        itemLS = item.getLSRate()
        itemHB = item.getHBRate()
        itemByno = item.getBynoMinPrice()
        itemBuff = item.getBuffLS()

        buff90 = float(itemBuff)*0.9
        discount_10 = float(itemByno)*0.9
        #offer = math.floor(min(buff90, discount_10)/5)*5
        offer = item.getBynoMinPrice() // 2 + 5
        if counterOffer:
            self._offer(value=offer)
            return
        else:
            self._buy()
        
    def _buy(self):
        buy_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-bng-red.btn-lg.fastBuy.font-weight-bolder.w-100")))
        buy_button.click()

        set_trade_url_dropdown = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select.form-control option:first-child")))
        select = Select(set_trade_url_dropdown)
        select.select_by_index(1)

        complete_buying_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-block.btn-bng-green.btn-lg.font-weight-bolder.mb-2.mt-3.py-3")))
        print(complete_buying_btn.text)
        #complete_buying_btn.click()
    
    def _offer(self, value:float):
        offer_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-lg.btn-outline-dark.offer.w-100")))
        offer_button.click()
        
        offer_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='Fiyat']")))
        offer_field.send_keys(value)

        set_trade_url_dropdown = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select.form-control option:first-child")))
        select = Select(set_trade_url_dropdown)
        select.select_by_index(1)
        