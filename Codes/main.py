from byno import ByNoGame
from gamesatis import GameSatis


def data_fetch_process():
    #processGamesatis()
    processByno()

def processByno():
    bynoObject = ByNoGame()
    bynoObject.getLatestItems()

def processGamesatis():
    gamesatisobj = GameSatis()
    gamesatisobj.updateItems()

if __name__ == "__main__":
    data_fetch_process()