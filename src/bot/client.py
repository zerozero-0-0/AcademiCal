from tracemalloc import start
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

from src.bot.commands.add import Add
from src.bot.commands.done import DoneView
from src.bot.commands.list import create_task_list
from src.database.operations import DB_Check_Pending
from src.notifications.scheduler import start_class_end_notification_scheduler

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
        
    async def on_ready(self) -> None:
        print(f'{self.user} としてDiscordに接続しました!') 
        
        await self.tree.sync()
        assert CHANNEL_ID is not None
        channel = self.get_channel(int(CHANNEL_ID))
        if channel:
            await channel.send("Botが起動しました!")
        else:
            print(f"チャンネルID {self.channel_id} が見つかりません。設定を確認してください。")
    
        try:
            await start_class_end_notification_scheduler(self)       
        except Exception as e:
            print(f"授業終了通知のスケジューラーの開始に失敗しました: {e}")     
        
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return
        
        print(f'{message.author} からメッセージを受信しました: {message.content}')
        
    def run_bot(self) -> None:
        assert self.discord_token is not None
        self.run(self.discord_token)
        
def MakeClient() -> MyClient:
    client = MyClient()
    
    @client.tree.command(name="add", description="課題追加")
    async def modal_command(interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(Add())
        
    @client.tree.command(name="list", description="課題一覧を表示")
    async def list_command(interaction: discord.Interaction) -> None:
        embed = create_task_list()
        await interaction.response.send_message(embed=embed)

    @client.tree.command(name="done", description="未完了の課題を完了にする")
    async def done_command(interaction: discord.Interaction):
        tasks = DB_Check_Pending()
        if not tasks:
            await interaction.response.send_message(
                "課題はありません。", ephemeral=True
            )
            return

        embed = discord.Embed(title="課題一覧")
        for task in tasks:
            id, title, description, due_date, status = task
            embed.add_field(
                name=title,
                value=f"締切: {due_date} / 状態: {'完了' if status == 'completed' else '未完了'}",
                inline=False,
            )
        view = DoneView(tasks)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    return client
