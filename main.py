import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from src.utils.read_json import read_json
from src.database import DB_Connect
from src.bot import MyClient

def main(): 
    load_dotenv()
    
    bot = MyClient(intents=discord.Intents.default())
    bot.run_bot()

if __name__ == "__main__":
    main()
