import discord
from src.database import DB_Done

"""
doneメソッドの関数
モーダルの表示 -> 未完了の課題を表示 -> 完了したかどうかをGUIで確認 -> 変更をDBに適用 
"""
class DoneSelect(discord.ui.Select):
    def __init__(self, tasks):
        options = []
        for task in tasks:
            id, title, description, due_date, status = task
            options.append(
                discord.SelectOption(
                    label=title,
                    description=f"締切: {due_date}",
                    value=str(id),
                    default=(status == "completed")
                )
            )
        super().__init__(
            placeholder="完了した課題を選択してください",
            min_values=0,
            max_values=len(options),
            options=options
        )
        self.selected_ids = set()

    async def callback(self, interaction: discord.Interaction):
        self.selected_ids = set(self.values)
        await interaction.response.defer()

class DoneView(discord.ui.View):
    def __init__(self, tasks):
        super().__init__(timeout=600)
        self.select = DoneSelect(tasks)
        self.add_item(self.select)
        self.add_item(SendButton(self))

class SendButton(discord.ui.Button):
    def __init__(self, view):
        super().__init__(label="送信", style=discord.ButtonStyle.success)
        self.parent_view = view
        
    async def callback(self, interaction: discord.Interaction) -> None:
        for task_id in self.parent_view.select.selected_ids:
            DB_Done(task_id)
        await interaction.response.send_message("選択した課題を完了にしました。", ephemeral=True)
