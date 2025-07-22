import asyncio
from datetime import datetime
import discord
import os

from src.utils.add import Add
from src.utils.getWeek import GetWeek
from src.utils.read_json import read_json
from src.utils.scheduler import get_subject_by_period


CHANNEL_ID = os.getenv("CHANNEL_ID")

class TaskAddView(discord.ui.View):
    """課題追加確認用のビュー"""

    def __init__(self, task_title: str):
        super().__init__(timeout=300)
        self.task_title = task_title
        
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success, emoji="✅")
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Yesボタンが押されたときの処理"""
        await interaction.response.send_modal(Add(subject_name=self.task_title))
        
    @discord.ui.button(label="No", style=discord.ButtonStyle.danger, emoji="❌")
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Noボタンが押されたときの処理"""
        await interaction.response.send_message(
            "課題追加をキャンセルしました。",
            ephemeral=True
        )
        self.stop()

async def send_class_and_notification(client: discord.Client, task_title: str):
    """
    課題追加の確認メッセージを送信し、ユーザーの応答を待つ
    Args:
        client (discord.Client): Discordクライアント
        task_title (str): 課題のタイトル
    """
    assert CHANNEL_ID is str
    channel_id = int(CHANNEL_ID)
    channel = client.get_channel(channel_id)
    
    if not channel:
        print(f"チャンネルID {channel_id} が見つかりません。")
        return

    embed = discord.Embed(
        title="授業完了通知",
        description=f"**{task_title}** の授業が終了しました!",
        color=0x00ff00,
        timestamp=datetime.now()
    )
    embed.add_field(
        name="課題追加",
        value=f"{task_title} の課題を追加しますか？",
        inline=False
    )
    
    view = TaskAddView(task_title)
    
    await channel.send(embed=embed, view=view)
    
async def check_and_send_notification(client: discord.Client, channel_id: int):
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_weekday = GetWeek()
    
    timetable = read_json("dataset/timetable.json")
    period_data = read_json("dataset/period.json")
    
    if not timetable or not period_data:
        print("タイムテーブルまたは期間データが読み込めませんでした。")
        return
    
    for period_num in range(1, 6):
        period_str = str(period_num)
        end_time = period_data[period_str]["end_time"]
        
        if current_time == end_time:
            subject_name = get_subject_by_period(timetable, current_weekday, period_num)
            
            if subject_name and subject_name.strip() != "":
                await send_class_and_notification(client, subject_name)
                
                
async def start_class_end_notification_scheduler(client: discord.Client):
    """
    授業終了通知のスケジューラーを開始
    Args:
        client (discord.Client): Discordクライアント
    """
    print("授業終了通知スケジューラーを開始します...")
    
    # 定期的に授業終了通知をチェック
    while True:
        await check_and_send_notification(client, int(os.getenv("CHANNEL_ID")))
        await asyncio.sleep(60)  # 1分ごとにチェック
                
            
            
        
