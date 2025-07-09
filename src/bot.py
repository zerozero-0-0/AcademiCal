
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
        channel = self.get_channel(int(self.channel_id))
        if channel:
            await channel.send("Botが起動しました!")
        else:
            print(f"チャンネルID {self.channel_id} が見つかりません。設定を確認してください。")
        
    def run_bot(self):
        self.run(self.discord_token)

