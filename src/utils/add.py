import re
from datetime import datetime, timedelta

import discord

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
        placeholder="課題名",  # 将来的に[授業名][第n回レポート]にする
        required=True,
    )

    task_description = discord.ui.TextInput(
        label="課題の説明を入力してください",
        style=discord.TextStyle.long,
        required=False,
    )

    task_due_date = discord.ui.TextInput(
        label="締切日を入力", style=discord.TextStyle.short, default=time, required=True
    )

    def __init__(self, subject_name: str = None) -> None:
        super().__init__(
            title=f"AcademiCal Modal{f' - {subject_name}' if subject_name else ''}"
        )
        self.subject_name = subject_name

        # subject_nameが指定されている場合、課題名のplaceholderを更新
        if subject_name:
            self.task_title.placeholder = f"[{subject_name}] 課題名"

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if not re.match(r"^\d{1,2}/\d{1,2} \d{1,2}:\d{2}$", self.task_due_date.value):
            await interaction.response.send_message(
                "締切日は「MM/DD HH:MM」の形式で入力してください。", ephemeral=True
            )
            return

        # 課題名にsubject_nameを自動で含める（科目名が指定されている場合）
        task_title = self.task_title.value
        if self.subject_name and not task_title.startswith(f"[{self.subject_name}]"):
            task_title = f"[{self.subject_name}] {task_title}"

        DB_Insert(
            title=task_title,
            description=self.task_description.value,
            due_data=self.task_due_date.value,
        )

        await interaction.response.send_message(f"課題「{task_title}」を登録しました")
