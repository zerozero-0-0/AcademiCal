
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from src.utils.add import Add
from src.utils.task_list import create_task_list
from src.database import DB_Check_All
from src.utils.done import DoneView

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not DISCORD_TOKEN and not CHANNEL_ID:
    raise ValueError("DISCORD_TOKEN または CHANNEL_ID が設定されていません")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN が設定されていません")

if not CHANNEL_ID:
    raise ValueError("CHANNEL_ID が設定されていません")



class MyClient(commands.Bot):
    def __init__(self, command_prefix='!', intents=None):
        self.discord_token = DISCORD_TOKEN
        self.channel_id = CHANNEL_ID
        
        intents = discord.Intents.default()
        intents.message_content = True
        
                                
        super().__init__(command_prefix, intents=intents)
    
    async def on_ready(self):
        print(f'{self.user} としてDiscordに接続しました!') 
        
        await self.tree.sync()
        channel = self.get_channel(int(CHANNEL_ID))
        if channel:
            await channel.send("Botが起動しました!")
        else:
            print(f"チャンネルID {self.channel_id} が見つかりません。設定を確認してください。")
        
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        
        print(f'{message.author} からメッセージを受信しました: {message.content}')
        
    def run_bot(self):
        self.run(self.discord_token) 

def MakeClient() -> MyClient:
    client = MyClient()
    
    @client.tree.command(name="add", description="課題追加用のモーダル")
    async def modal_command(interaction: discord.Interaction):
        await interaction.response.send_modal(Add())
    
    #
    @client.tree.command(name="list", description="登録されている課題の一覧を表示")
    async def list_command(interaction: discord.Interaction):
        embed = create_task_list()
        await interaction.response.send_message(embed=embed)
        
    @client.tree.command(name="done", description="未完了の課題を完了にする")
    async def done_command(interaction: discord.Interaction):
        tasks = DB_Check_All()
        if not tasks:
            await interaction.response.send_message("課題はありません。", ephemeral=True)
            return
        
        embed = discord.Embed(title="課題一覧")
        for task in tasks:
            id, title, description, due_date, status = task
            embed.add_field(
                name=title,
                value=f"締切: {due_date} / 状態: {'完了' if status == 'completed' else '未完了'}",
                inline=False
            )
        view = DoneView(tasks)
        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True
        )

    return client
