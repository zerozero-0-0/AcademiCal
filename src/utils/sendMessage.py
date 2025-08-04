import re
from src.data.read_json import read_json
from src.utils.scheduler import get_subject_by_period
from datetime import datetime, timedelta
import discord

def sendMessage(idx, next_notice_time) -> None:
    """
    メッセージを送信する関数
    Args:
        idx (int): 時間目のインデックス
        next_notice_time (str): 次に通知を送る時間
    Returns:
        None
    """
    subject = get_subject_by_period(read_json("dataset/timetable.json"), "week", idx)
    
    if subject:
        message = f"次の授業は {subject} です。時間: {next_notice_time}"
       
       
current_time = datetime.now() + timedelta(days=7)

time = current_time.strftime("%m/%d %H:%M")

class Notification(discord.ui.Modal):
    task_title = discord.ui.TextInput(
        label="課題名を入力",
        style=discord.TextStyle.short,
        required=True
    )
    
    task_description = discord.ui.TextInput(
        label="課題の説明を入力してください",
        style=discord.TextStyle.long,
        required=False
    )
    
    task_due_date = discord.ui.TextInput(
        label="締切日を入力",
        style=discord.TextStyle.short,
        default=time,
        required=True
    )

    def __init__(self) -> None:
        super().__init__(title="AcademiCal Notification")
        
    async def on_submit(self, interaction: discord.Interaction) -> None:
        if not re.match(r"^\d{1,2}/\d{1,2} \d{1,2}:\d{2}$", self.task_due_date.value):
            await interaction.response.send_message(
                "締切日は「MM/DD HH:MM」の形式で入力してください。",
                ephemeral=True
            )
            return
        
        sendMessage(self.task_title.value, self.task_due_date.value)
        await interaction.response.send_message(
            f"課題 {self.task_title.value} を登録しました"
        )
