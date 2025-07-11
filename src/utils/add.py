import discord
from discord.ext import commands
import os
from datetime import datetime, timedelta
from src.database import DB_Insert

# 1. GUIを表示
# 2. 入力を受け取る
# 3. 入力内容をdbに適用

current_time = datetime.now() + timedelta(days=7)

time = current_time.strftime("%m/%d %H:%M")

class Add(discord.ui.Modal):
    task_title = discord.ui.TextInput(
        label="課題名を入力",
        style=discord.TextStyle.short,
        placeholder="課題名",
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
        placeholder=time,
        required=True
    )

    def __init__(self) -> None:
        super().__init__(title="AcademiCal Modal")
        
    async def on_submit(self, interaction: discord.Interaction) -> None:
        DB_Insert(
            title=self.task_title.value,
            description=self.task_description.value,
            due_data=self.task_due_date.value
        )
        await interaction.response.send_message(
            f"課題{self.task_title.value}を登録しました"
        )
        