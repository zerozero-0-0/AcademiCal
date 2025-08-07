from datetime import datetime, timedelta
from typing import Optional

import discord

from src.database.operations import DB_Insert
from src.ui.components.calendar import CalendarView

# 1. GUIを表示
# 2. 入力を受け取る
# 3. 入力内容をdbに適用

current_time = datetime.now() + timedelta(days=7)

time = current_time.strftime("%m/%d %H:%M")


class ConfirmAddView(discord.ui.View):
    def __init__(self, task_title, task_description, selected_date, on_confirm):
        super().__init__(timeout=60)
        self.task_title = task_title
        self.task_description = task_description
        self.selected_date = selected_date
        self.on_confirm = on_confirm

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success)
    async def yes_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.on_confirm(interaction, True)
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def no_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.on_confirm(interaction, False)
        self.stop()


class Add(discord.ui.Modal):
    # task_title = discord.ui.TextInput(
    #     label="課題名を入力",
    #     style=discord.TextStyle.short,
    #     placeholder="課題名",  # 将来的に[授業名][第n回レポート]にする
    #     default="",
    #     max_length=30,
    #     required=True,
    # )

    # task_description = discord.ui.TextInput(
    #     label="課題の説明を入力してください",
    #     style=discord.TextStyle.short,
    #     max_length=100,
    #     required=False,
    # )

    # task_due_date = discord.ui.TextInput(
    #     label="締切日を入力", style=discord.TextStyle.short, default=time, required=True
    # )

    def __init__(self, subject_name: Optional[str] = None) -> None:
        super().__init__(
            title=f"AcademiCal Modal{f' - {subject_name}' if subject_name else ''}"
        )
        self.subject_name = subject_name

        if subject_name:
            placeholder_txt = f"[{subject_name}]"
            default_txt = f"{placeholder_txt}"
        else:
            placeholder_txt = "課題名"
            default_txt = ""

        self.task_title = discord.ui.TextInput(
            label="課題名を入力",
            style=discord.TextStyle.short,
            placeholder=placeholder_txt,
            default=default_txt,
            max_length=30,
            required=True,
        )

        self.task_description = discord.ui.TextInput(
            label="課題の説明を入力してください",
            style=discord.TextStyle.short,
            max_length=100,
            required=False,
        )

        self.add_item(self.task_title)
        self.add_item(self.task_description)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        # if not re.match(r"^\d{1,2}/\d{1,2} \d{1,2}:\d{2}$", self.task_due_date.value):
        #     await interaction.response.send_message(
        #         "締切日は「MM/DD HH:MM」の形式で入力してください。", ephemeral=True
        #     )
        #     return

        task_title_input = self.task_title.value
        task_description_input = self.task_description.value or ""

        # 科目名が指定されている場合
        if self.subject_name and not task_title_input.startswith(
            f"[{self.subject_name}]"
        ):
            final_task_title = f"[{self.subject_name}]{task_title_input}"
        else:
            final_task_title = task_title_input

        self.task_title_value = final_task_title
        self.task_description_value = task_description_input

        calendar_view = CalendarView(callback=self.on_date_selected)
        embed = calendar_view._create_calendar_embed()

        embed.add_field(
            name="課題情報",
            value=f"**課題名:** {self.task_title_value}\n"
            f"**説明:** {self.task_description_value or 'なし'}\n",
            inline=False,
        )
        embed.add_field(
            name="次のステップ", value="日付を選択してください", inline=False
        )

        # DB_Insert(
        #     title=task_title,
        #     description=self.task_description.value,
        #     due_data=self.task_due_date.value,
        # )

        await interaction.response.send_message(
            embed=embed, view=calendar_view, ephemeral=True
        )

    async def on_date_selected(
        self, interaction: discord.Interaction, selected_date: datetime
    ):
        """日付が選択されたときの処理（確認Viewを表示）"""
        task_title = self.task_title_value
        task_description = self.task_description_value
        date_str = selected_date.strftime("%Y年%m月%d日")
        confirm_msg = f"{date_str}で『{task_title}』を追加しますか？ "

        async def on_confirm(confirm_interaction, is_yes):
            if is_yes:
                DB_Insert(
                    title=task_title,
                    description=task_description,
                    due_data=selected_date.strftime("%m/%d %H:%M"),
                )
                embed = discord.Embed(
                    title="課題を追加しました",
                    description=f"**課題名:** **{task_title}**\n"
                    f"**説明:** **{task_description or 'なし'}**\n"
                    f"**締切日:** **{selected_date.strftime('%Y年%m月%d日 %H:%M')}**",
                    color=0x00FF00,
                )
                await confirm_interaction.response.edit_message(
                    content=None, embed=embed, view=None
                )
            else:
                await confirm_interaction.response.edit_message(
                    content="課題追加をキャンセルしました。", embed=None, view=None
                )

        view = ConfirmAddView(task_title, task_description, selected_date, on_confirm)
        await interaction.response.send_message(
            content=confirm_msg, view=view, ephemeral=True
        )
