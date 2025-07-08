import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

class Client(discord.Client):
    async def on_ready(self):
        print(f'{self.user} として接続しました')
        
    async def on_message(self, message):
        print(f'{message.author} からのメッセージ: {message.content}')

def main():
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    if not (DISCORD_TOKEN and CHANNEL_ID):
        print("DISCORD_TOKEN または CHANNEL_ID が設定されていません")
        return
    
    intents = discord.Intents.default()
    intents.message_content = True  # メッセージの内容を取得する権限を付与
    
    client = Client(intents=intents)
    client.run(DISCORD_TOKEN)
        
    
if __name__ == "__main__":
    main()
    
