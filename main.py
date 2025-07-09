import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from src.utils.read_json import read_json
from src.database import DB_Connect

def main(): 
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    if not (DISCORD_TOKEN and CHANNEL_ID):
        print("DISCORD_TOKEN または CHANNEL_ID が設定されていません")
        return
    
    intents = discord.Intents.default()
    intents.message_content = True  # メッセージの内容を取得する権限を付与

    bot = commands.Bot(
        command_prefix="!",
        case_intesitive=False,
        intents=intents
    )
    
    @bot.event
    async def on_ready():
        print("接続に成功しました")

def read_json_test():
    data = read_json(".dataset/.peroid.json")
    if data:
        print(data)
    else:
        print("JSONファイルの読み込みに失敗しました")

if __name__ == "__main__":
    DB_Connect()
    read_json_test()
    main()
