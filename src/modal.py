import discord
from discord.ext import commands
import os

# 1. GUIを表示
# 2. 入力を受け取る
# 3. 入力内容をdbに適用

class Modal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title="AcademiCal Modal", timeout=None, custom_id="academical_modal")
        
        self.text1 = discord.ui.TextInput(label="Example Input Field")
        self.text2 = discord.ui.TextInput(
            label="Example Long Input Field",
            style=discord.TextStyle.long
        )
        
        self.add_item(self.text1)
        self.add_item(self.text2)
        
    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            f"{self.text1.value} and {self.text2.value} を送信しました"
        )
        