from datetime import datetime, timedelta
from typing import Optional

import discord


class CalendarView(discord.ui.View):
    def _create_calendar_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=f"📅 {self.year}年 {self.month}月",
            description="日付を選択してください",
            color=0x00FF00,
        )

        if self.selected_date:
            embed.add_field(
                name="選択された日付",
                value=self.selected_date.strftime("%Y年%m月%d日"),
                inline=False,
            )

        return embed

    def __init__(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        callback: Optional[callable] = None,
        page: int = 0,  # ページ番号追加
    ):
        super().__init__(timeout=300)
        now = datetime.now()
        self.start_date = now.date()
        self.end_date = (now + timedelta(days=90)).date()
        self.year = year or now.year
        self.month = month or now.month
        self.day = day or now.day
        self.selected_date = None
        self.callback = callback
        self.page = page  # ページ番号保持
        self._build_calendar()

    def _build_calendar(self):
        self.clear_items()
        self.add_item(PrevPageButton(self))
        self.add_item(PreviousMonthButton(self))
        self.add_item(CurrentMonthButton(self))
        self.add_item(NextMonthButton(self))
        self.add_item(NextPageButton(self))

        today = datetime.now().date()
        # 今週の月曜日を取得
        start = today - timedelta(days=today.weekday())
        # 週ごと（月〜金）に分ける（1行目は必ず今週の月〜金、過去日も含めて曜日位置を揃える）
        weeks = []
        week_start = start
        # 1行目: 今週の月〜金
        week = []
        for i in range(5):
            day = week_start + timedelta(days=i)
            if day <= self.end_date:
                week.append(day)
        if week:
            weeks.append(week)
        # 2行目以降: 翌週以降の月〜金
        week_start += timedelta(days=7)
        while week_start <= self.end_date:
            week = []
            for i in range(5):
                day = week_start + timedelta(days=i)
                if day <= self.end_date:
                    week.append(day)
            if week:
                weeks.append(week)
            week_start += timedelta(days=7)
        # ページごとに4週分のみ表示（row=1〜4）
        page_size = 4
        start_idx = self.page * page_size
        end_idx = start_idx + page_size
        for row, week in enumerate(weeks[start_idx:end_idx]):
            if row >= 4:
                break  # row=4以上は追加しない
            for col, date_obj in enumerate(week):
                is_past = date_obj < today
                self.add_item(DateButton(date_obj, self, row=row + 1, is_past=is_past))

    def _get_available_dates(self) -> list:
        """利用可能な日付を取得"""
        available_dates = []
        current_date = self.start_date
        while current_date <= self.end_date:
            available_dates.append(current_date)
            current_date += timedelta(days=1)
        return available_dates

    def _get_week_buttons(self, count=7):
        """週のボタンを取得（必要数だけ返す）"""
        weeks = []
        for i in range(count):
            week_date = self.start_date + timedelta(days=i)
            weeks.append(DateButton(week_date, self))
        return weeks


# --- ここからボタンクラス定義 ---
class PreviousMonthButton(discord.ui.Button):
    def __init__(self, calendar_view):
        super().__init__(label="<", style=discord.ButtonStyle.secondary, row=0)
        self.calendar_view = calendar_view

    async def callback(self, interaction: discord.Interaction):
        if self.calendar_view.month == 1:
            self.calendar_view.month = 12
            self.calendar_view.year -= 1
        else:
            self.calendar_view.month -= 1
        self.calendar_view._build_calendar()
        await interaction.response.edit_message(view=self.calendar_view)


class CurrentMonthButton(discord.ui.Button):
    def __init__(self, calendar_view):
        super().__init__(label="今月", style=discord.ButtonStyle.primary, row=0)
        self.calendar_view = calendar_view

    async def callback(self, interaction: discord.Interaction):
        now = datetime.now()
        self.calendar_view.year = now.year
        self.calendar_view.month = now.month
        self.calendar_view._build_calendar()
        await interaction.response.edit_message(view=self.calendar_view)


class NextMonthButton(discord.ui.Button):
    def __init__(self, calendar_view):
        super().__init__(label=">", style=discord.ButtonStyle.secondary, row=0)
        self.calendar_view = calendar_view

    async def callback(self, interaction: discord.Interaction):
        if self.calendar_view.month == 12:
            self.calendar_view.month = 1
            self.calendar_view.year += 1
        else:
            self.calendar_view.month += 1
        self.calendar_view._build_calendar()
        await interaction.response.edit_message(view=self.calendar_view)


class DateButton(discord.ui.Button):
    def __init__(self, date_obj, calendar_view, row=1, is_past=False):
        self.date_obj = date_obj
        self.calendar_view = calendar_view
        today = datetime.now().date()
        if is_past:
            style = discord.ButtonStyle.secondary
            disabled = True
        elif date_obj == today:
            style = discord.ButtonStyle.success
            disabled = False
        else:
            style = discord.ButtonStyle.primary
            disabled = False
        super().__init__(
            label=str(date_obj.day), style=style, row=row, disabled=disabled
        )

    async def callback(self, interaction: discord.Interaction):
        self.calendar_view.selected_date = self.date_obj
        # on_date_selectedがあれば呼び出す（Addモーダルから渡される）
        if hasattr(self.calendar_view, "callback") and self.calendar_view.callback:
            await self.calendar_view.callback(interaction, self.date_obj)
        else:
            await interaction.response.send_message(
                f"選択された日付: {self.date_obj}", ephemeral=True
            )


class PrevPageButton(discord.ui.Button):
    def __init__(self, calendar_view):
        super().__init__(label="<<", style=discord.ButtonStyle.secondary, row=0)
        self.calendar_view = calendar_view

    async def callback(self, interaction: discord.Interaction):
        if self.calendar_view.page > 0:
            self.calendar_view.page -= 1
            self.calendar_view._build_calendar()
            await interaction.response.edit_message(view=self.calendar_view)
        else:
            await interaction.response.defer()


class NextPageButton(discord.ui.Button):
    def __init__(self, calendar_view):
        super().__init__(label=">>", style=discord.ButtonStyle.secondary, row=0)
        self.calendar_view = calendar_view

    async def callback(self, interaction: discord.Interaction):
        today = datetime.now().date()
        # 今週の月曜日を取得
        start = today - timedelta(days=today.weekday())
        # 週ごと（月〜金）に分ける
        weeks = []
        week_start = start
        end_date = self.calendar_view.end_date
        while week_start <= end_date:
            week = []
            for i in range(5):
                day = week_start + timedelta(days=i)
                if (
                    day >= self.calendar_view.start_date
                    and day <= end_date
                    and day.weekday() < 5
                ):
                    week.append(day)
            if week:
                weeks.append(week)
            week_start += timedelta(days=7)
        total_pages = (len(weeks) + 3) // 4  # 1ページ=4週分
        if self.calendar_view.page < total_pages - 1:
            self.calendar_view.page += 1
            self.calendar_view._build_calendar()
            await interaction.response.edit_message(view=self.calendar_view)
        else:
            await interaction.response.defer()
