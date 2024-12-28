from item import Item
from tqdm import tqdm
import json
import sqlite3
from helpers import CONSTANTS, Items, Platforms

db_path = "Settings/database.db"

def createSQL():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        name TEXT PRIMARY KEY,
        image TEXT DEFAULT NULL,
        buff JSON DEFAULT NULL,
        bynogame JSON DEFAULT NULL,
        gamesatis JSON DEFAULT NULL
    )
    ''')

    conn.commit()
    conn.close()

def createProfitSQL():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profitables (
        name TEXT DEFAULT NULL,
        image TEXT DEFAULT NULL,
        buff JSON DEFAULT NULL,
        info JSON DEFAULT NULL UNIQUE,
        platform TEXT DEFAULT NULL
    )
    ''')

    conn.commit()
    conn.close()

def create_item(name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert a new item with only the name
    cursor.execute('''
        INSERT OR IGNORE INTO items (name) VALUES (?)
    ''', (name,))

    conn.commit()
    conn.close()
    tqdm.write(f"Item '{name}' has been created.")

def update_item(item:Item, platform:Platforms):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    updates = []
    values = []
    name = item.getName()
    
    match platform:
        case Platforms.BUFF:
            data = item.getBuffData()
            updates.append("buff = ?")
        case Platforms.BYNOGAME:
            data = item.getBynoGameData()
            updates.append("bynogame = ?")
        case Platforms.GAMESATIS:
            data = item.getGamesatisData()
            updates.append("gamesatis = ?")
        case _:
            tqdm.write(f"Platform does not exist: {platform}")
            return
    
    values.append(json.dumps(data))

    image = item.getImageURL()
    if image:
        updates.append("image = ?")
        values.append(image)

    # Add the name to the values list for the WHERE clause
    values.append(name)

    # Construct the query
    query = f'''
        UPDATE items
        SET {", ".join(updates)}
        WHERE name = ?
    '''

    cursor.execute(query, values)
    conn.commit()
    conn.close()
    tqdm.write(f"[UPDATE] {platform:<10} | {item}")

    match platform:
        case Platforms.BYNOGAME:
            rate = data.get(Items.RATES.BynoGame_LS)
            price = data.get(Items.PRICES.BynoGame)
        case Platforms.GAMESATIS:
            rate = data.get(Items.RATES.Gamesatis_LS)
            price = data.get(Items.PRICES.Gamesatis)
        case _:
            rate = None
            price = None

    if data and rate and rate < CONSTANTS.THRESHOLDS.lowestSellRate and price > CONSTANTS.THRESHOLDS.minprice:
        copy_item_to_profitables(name, platform)

def get_all_profitables() -> list[tuple]:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Retrieve all items from the profitables table
        cursor.execute("SELECT * FROM profitables")
        all_items = cursor.fetchall()

        # Delete all items from the profitables table
        cursor.execute("DELETE FROM profitables")
        conn.commit()

        return all_items
    except Exception as e:
        tqdm.write(f"[ERROR] Failed to fetch and clear profitables: {e}")
        return []
    finally:
        conn.close()

def copy_item_to_profitables(name: str, platform: Platforms):
    match platform:
        case Platforms.BYNOGAME:
            insert = "bynogame"
        case Platforms.GAMESATIS:
            insert = "gamesatis"
        case _:
            raise Exception("Platform does not exist. Line 148 database.py")
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Copy the item from items to profitables
        cursor.execute(f'''
            INSERT OR IGNORE INTO profitables (name, image, buff, info, platform)
            SELECT name, image, buff, {insert}, ?
            FROM items
            WHERE name = ?;
        ''', (platform, name,))

        conn.commit()
    except Exception as e:
        tqdm.write(f"[ERROR] Failed to copy item '{name}' to profitables table: {e}")
    finally:
        conn.close()

def _toItem(info:tuple) -> Item | None:
    try:
        name, image, buff, bynogame, gamesatis = info
        # Parse JSON fields
        buff = json.loads(buff)
        bynogame = json.loads(bynogame)
        gamesatis = json.loads(gamesatis)

        item = Item(name=name)
        item.setImageURL(url=image)
        item.setBuffData(data=buff)
        item.setBynoGameData(data=bynogame)
        item.setGamesatisData(data=gamesatis)
        return item
    except Exception as e:
        tqdm.write(f"{e}\n\t--> Cannot convert to an Item object.")
    
def get_item(name:str) -> Item | None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM items WHERE name = ?', (name,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return _toItem(result)
    else:
        return None

def get_all_items() -> list[Item]:
    # Retrieve all items from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query all items from the database
    cursor.execute("SELECT * FROM items")
    all_items = cursor.fetchall()
    return [_toItem(item) for item in all_items]

createProfitSQL()