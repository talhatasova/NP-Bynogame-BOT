from python_whatsapp_bot import Whatsapp
from python_whatsapp_bot import Inline_keyboard, Inline_list, List_item

from dotenv import load_dotenv, dotenv_values
from item import Item
import os


class WhatsappBOT(Whatsapp):

    def __init__(self) -> None:
        load_dotenv()
        self.phone_id = os.getenv("PHONE_NUMBER_ID")
        self.token = os.getenv("TOKEN")
        self.version = os.getenv("VERSION")
        super().__init__(self.phone_id, self.token, self.version)

    def welcome(self):
        self.send_template_message("905422042004", "hello_world")

    def sendSkinInfo(self, item:Item):
        #reply_markup=Inline_keyboard(['url1', 'url2'])
        self.send_message("905422042004", item.getWhatsappMessage())
        #self.send_message("4915510564756", 'This is a message with lists', reply_markup=Inline_list("Show list",list_items=[List_item("one list item")]))
