from datetime import datetime
import json
from dotenv import load_dotenv
from discord import Intents, Message, Embed
from discord.ext import commands
import os
import asyncio

from tqdm import tqdm
from main import data_fetch_process
from helpers import CONSTANTS
import discord
from database import get_all_profitables

load_dotenv()
app_id = os.getenv("APP_ID")
token = os.getenv("DC_BOT_TOKEN")
public_key = os.getenv("PUBLIC_KEY")
bot_channel_id = int(os.getenv("NP_CHANNEL_ID"))

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Function to send messages based on user input
async def send_message(msg: Message, user_msg: str) -> None:
    if not user_msg:
        return
    try:
        await msg.channel.send(user_msg)
    except Exception as e:
        tqdm.write(e)

# Event to signal when the bot is ready
@bot.event
async def on_ready() -> None:
    tqdm.write(f"{bot.user} is running...")

async def sendEmbedMessage(name:str, buff_price, price, lsrate, hbrate, image, buff_url, url, platform_name, floatVal):
    embed = Embed(title="💰 PROFIT ALERT 💰", color=0x06f502, timestamp=datetime.now())
    embed.add_field(name=f"🛒 {name}",
                value=f"""
                    **Float**: {floatVal}

                    **💸 {platform_name} Price**: {price}₺
                    **💸 Buff163 Price**: {buff_price}₺

                    **📉 Lowest Sell Rate**: {lsrate}%
                    **📈 Highest Buy Rate**: {hbrate}%
                """, inline=False)
    embed.set_footer(text="PriceCheckerBOT v1.2 BETA")
    embed.set_thumbnail(url=image)    

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label=platform_name, url=url, emoji="💰"))
    view.add_item(discord.ui.Button(label="BUFF163", url=buff_url, emoji="💰"))

    channel = await bot.fetch_channel(bot_channel_id)
    if channel:
        await channel.send(embed=embed, view=view)

async def getDiscordMessage():
    profit_items = get_all_profitables()
    for item in profit_items:
        name, image, buff, info, platform_name = item
        buff:dict = json.loads(buff)
        info:dict = json.loads(info)
        floatVal = info.get("float", -1.0)
        price = info.get("price", None)
        url = info.get("url", "https://github.com/404")
        lsrate = info.get("ls_rate", float("inf"))
        hbrate = info.get("hb_rate", float("inf"))
        buff_price = buff.get("price_ls", float("inf"))
        buff_url = buff.get("url", "https://github.com/404")
        await sendEmbedMessage(name, buff_price, price, lsrate, hbrate, image, buff_url, url, platform_name, floatVal)


# Fetch and process data asynchronously
async def fetch_and_process_data():
    while True:
        data_fetch_process()
        await getDiscordMessage()
        await asyncio.sleep(CONSTANTS.update_interval_seconds)

# Main async function to run both bot and data fetching
async def main():
    await asyncio.gather(
        bot.start(token),
        fetch_and_process_data())

if __name__ == "__main__":
    asyncio.run(main())