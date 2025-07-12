import discord
from src.database import DB_Done, DB_Check_All
from dataclasses import dataclass

"""
doneメソッドの関数
モーダルの表示 -> 未完了の課題を表示 -> 完了したかどうかをGUIで確認 -> 変更をDBに適用 
"""
class DoneView(discord.ui.View):
    def __init__(self, tasks):
        super().__init__(timeout=600)
        self.completed_ids = set()
        for task in tasks:
            id, title, description, due_date, status = task
            self.add_item(DoneButton(label=title, task_id=id, view=self))

        self.add_item(SendButton(view=self))

class DoneButton(discord.ui.Button):
    def __init__(self, label, task_id, view):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.task_id = task_id
        self.parent_view = view

    async def callback(self, interaction: discord.Interaction):
        self.parent_view.completed_ids.add(self.task_id)
        await interaction.response.send_message(f"{self.label} を完了リストに追加しました", ephemeral=True)

class SendButton(discord.ui.Button):
    def __init__(self, view):
        super().__init__(label="送信", style=discord.ButtonStyle.success)
        self.parent_view = view

    async def callback(self, interaction: discord.Interaction):
        # ここでDB更新
        for task_id in self.parent_view.completed_ids:
            DB_Done(task_id)
        await interaction.response.send_message("完了課題を一括更新しました", ephemeral=True)
