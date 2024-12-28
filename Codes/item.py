from helpers import Items
from datetime import datetime

class Item():

    def __init__(self, name:str) -> None:
        self.name:str = name

        self.buffID:int = None
        self.buffLS:float = None
        self.buffHB:float = None
        self.buffURL:str = None
        self.buffLastUpdate:datetime = None

        self.bynoPrice:float = None
        self.byno_LS_Rate:float = None
        self.byno_HB_Rate:float = None
        self.bynoURL:str = None
        self.bynoFloat:float = None
        self.bynoLastUpdate:datetime = None

        self.gamesatisPrice:float = None
        self.gamesatis_LS_Rate:float = None
        self.gamesatis_HB_Rate:float = None
        self.gamesatisURL:str = None
        self.gamesatisFloat:float = None
        self.gamesatisLastUpdate:datetime = None

        self.imageURL:str = None
    
    def getBuffData(self) -> dict:
        return {
            Items.BUFF_ID: self.getBuffID(),
            Items.PRICES.Buff_LS: self.getBuffLS(),
            Items.PRICES.Buff_HB: self.getBuffHB(),
            Items.URLS.Buff: self.getBuffURL(),
            Items.UPDATE.Buff: self.getBuffLastUpdate()
        }
    
    def setBuffData(self, data:dict=None):
        if not data:
            return
        self.setBuffID(itemid=data.get(Items.BUFF_ID))
        self.setBuffLS(buffLS=data.get(Items.PRICES.Buff_LS))
        self.setBuffHB(buffHB=data.get(Items.PRICES.Buff_HB))
        self.setBuffURL(url=data.get(Items.URLS.Buff))
        self.setBuffLastUpdate(date=data.get(Items.UPDATE.Buff))

    def getBynoGameData(self) -> dict:
        return {
            Items.PRICES.BynoGame: self.getBynoPrice(),
            Items.URLS.BynoGame: self.getBynoURL(),
            Items.RATES.BynoGame_LS: self.getBynoLSRate(),
            Items.RATES.BynoGame_HB: self.getBynoHBRate(),
            Items.FLOATS.BynoGame: self.getBynoFloat(),
            Items.UPDATE.Buff: self.getBynoLastUpdate(),
        }
    
    def setBynoGameData(self, data:dict=None):
        if not data:
            return
        self.setBynoPrice(price=data.get(Items.PRICES.BynoGame))
        self.setBynoURL(url=data.get(Items.URLS.BynoGame))
        self.setImageURL(url=data.get(Items.URLS.Image))
        self._setBynoLSRate()
        self._setBynoHBRate()
        self.setBynoFloat(floatVal=data.get(Items.FLOATS.BynoGame))
        self.setBynoLastUpdate(date=data.get(Items.UPDATE.BynoGame))

    def getGamesatisData(self) -> dict:
        return {
            Items.PRICES.Gamesatis: self.getGamesatisPrice(),
            Items.URLS.Gamesatis: self.getGamesatisURL(),
            Items.RATES.Gamesatis_LS: self.getGamesatisLSRate(),
            Items.RATES.Gamesatis_HB: self.getGamesatisHBRate(),
            Items.FLOATS.Gamesatis: self.getGamesatisFloat(),
            Items.UPDATE.Gamesatis: self.getGamesatisLastUpdate(),
        }

    def setGamesatisData(self, data:dict=None):
        if not data:
            return
        self.setGamesatisPrice(price=data.get(Items.PRICES.Gamesatis))
        self.setGamesatisURL(url=data.get(Items.URLS.Gamesatis))
        self.setImageURL(url=data.get(Items.URLS.Image))
        self._setGamesatisLSRate()
        self._setGamesatisHBRate()
        self.setGamesatisFloat(floatVal=data.get(Items.FLOATS.Gamesatis))
        self.setGamesatisLastUpdate(date=data.get(Items.UPDATE.Gamesatis))
    
    def getName(self) -> str:
        return self.name

    def setName(self, name: str) -> None:
        self.name = name

    def getBuffLS(self) -> float:
        return self.buffLS

    def setBuffLS(self, buffLS: float) -> None:
        self.buffLS = buffLS
        self._setBynoLSRate()
        self._setGamesatisLSRate()

    def getBuffHB(self) -> float:
        return self.buffHB

    def setBuffHB(self, buffHB: float) -> None:
        self.buffHB = buffHB
        self._setBynoHBRate()
        self._setGamesatisHBRate()

    def getBynoPrice(self) -> float:
        return self.bynoPrice

    def setBynoPrice(self, price: float) -> None:
        self.bynoPrice = price
        self._setBynoLSRate()
        self._setBynoHBRate()

    def getBynoLSRate(self) -> float:
        return self.byno_LS_Rate

    def _setBynoLSRate(self) -> None:
        if self.getBuffLS() is not None and self.getBynoPrice() is not None:
            self.byno_LS_Rate = round(self.getBynoPrice() / self.getBuffLS() * 100, 2)
        else:
            self.byno_LS_Rate = None

    def getBynoHBRate(self) -> float:
        return self.byno_HB_Rate

    def _setBynoHBRate(self) -> None:
        if self.getBuffHB() is not None and self.getBynoPrice() is not None:
            self.byno_HB_Rate = round(self.getBynoPrice() / self.getBuffHB() * 100, 2)
        else:
            self.byno_HB_Rate = None

    def getGamesatisPrice(self) -> float:
        return self.gamesatisPrice

    def setGamesatisPrice(self, price: float) -> None:
        self.gamesatisPrice = price
        self._setGamesatisLSRate()
        self._setGamesatisHBRate()

    def getGamesatisLSRate(self) -> float:
        return self.gamesatis_LS_Rate

    def _setGamesatisLSRate(self) -> None:
        if self.getBuffLS() is not None and self.getGamesatisPrice() is not None:
            self.gamesatis_LS_Rate = round(self.getGamesatisPrice() / self.getBuffLS() * 100, 2)
        else:
            self.gamesatis_LS_Rate = None

    def getGamesatisHBRate(self) -> float:
        return self.gamesatis_HB_Rate

    def _setGamesatisHBRate(self) -> None:
        if self.getBuffHB() is not None and self.getGamesatisPrice() is not None:
            self.gamesatis_HB_Rate = round(self.getGamesatisPrice() / self.getBuffHB() * 100, 2)
        else:
            self.gamesatis_HB_Rate = None

    def getBynoURL(self) -> str:
        return self.bynoURL

    def setBynoURL(self, url: str) -> None:
        self.bynoURL = url

    def getBuffURL(self) -> str:
        return self.buffURL

    def setBuffURL(self, url: str) -> None:
        self.buffURL = url

    def getGamesatisURL(self) -> str:
        return self.gamesatisURL

    def setGamesatisURL(self, url: str) -> None:
        self.gamesatisURL = url

    def getImageURL(self) -> str:
        return self.imageURL

    def setImageURL(self, url: str) -> None:
        self.imageURL = url

    def getBynoFloat(self) -> float:
        return self.bynoFloat

    def setBynoFloat(self, floatVal: float) -> None:
        try:
            value = round(float(floatVal), 6)
            self.bynoFloat = value
        except Exception as e:
            pass
    
    def getGamesatisFloat(self) -> float:
        return self.gamesatisFloat

    def setGamesatisFloat(self, floatVal: float) -> None:
        try:
            value = round(float(floatVal), 6)
            self.gamesatisFloat = value
        except Exception as e:
            pass
    
    def getBuffLastUpdate(self) -> str:
        return self.buffLastUpdate
    
    def setBuffLastUpdate(self, date:datetime):
        self.buffLastUpdate = date

    def getBynoLastUpdate(self) -> str:
        return self.bynoLastUpdate
    
    def setBynoLastUpdate(self, date:datetime):
        self.bynoLastUpdate = date

    def getGamesatisLastUpdate(self) -> str:
        return self.gamesatisLastUpdate
    
    def setGamesatisLastUpdate(self, date:datetime):
        self.gamesatisLastUpdate = date
    
    def getBuffID(self) -> int:
        return self.buffID
    
    def setBuffID(self, itemid:int) -> None:
        self.buffID = itemid

    def __repr__(self):
        name = f"{self.name!r}".ljust(50)
        price = f"{self.buffLS!r}".ljust(7)
        rate = f"{self.byno_LS_Rate!r}".ljust(6)

        return f"{name} | BuffLS={price} | BynoLSRate={rate}"
    
    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)