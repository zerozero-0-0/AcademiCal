
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os


class MyClient(discord.Client):
    def __init__(self, intents):
        self.discord_token = os.getenv("DISCORD_TOKEN")
        self.channel_id = os.getenv("CHANNEL_ID")
        
        if not (self.discord_token and self.channel_id):
            raise ValueError("DISCORD_TOKEN または CHANNEL_ID が設定されていません")
        
        intents = discord.Intents.default()
        intents.message_content = True  # メッセージの内容を取得する権限を付与
        
        super().__init__(intents=intents)
    
    async def on_ready(self):
        print(f'{self.user} としてDiscordに接続しました!')    
        
    def run_bot(self):
        self.run(self.discord_token)

load_dotenv()

# def Bot_Init():
#     DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
#     CHANNEL_ID = os.getenv("CHANNEL_ID")

#     if not (DISCORD_TOKEN and CHANNEL_ID):
#         print("DISCORD_TOKEN または CHANNEL_ID が設定されていません")
#         return

#     intents = discord.Intents.default()
#     intents.message_content = True  # メッセージの内容を取得する権限を付与

#     client = MyClient(intents=intents)
#     client.run(DISCORD_TOKEN)

# async def Bot_Notify(Class: str):
#     """
#     discordのチャンネルに課題を追加するかどうかを確認するメッセージを送る
#     Args:
#         Class (str): 授業名
#     Returns:
#         None
#     """
    
#     message = f"{Class}の課題を追加しますか?"
    
#     await client.send(message)

