import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from src.utils.read_json import read_json
from src.database import DB_Connect
from src.bot import MakeClient

def main(): 
    DB_Connect()
    
    client = MakeClient()
    client.run_bot()

if __name__ == "__main__":
    main()
