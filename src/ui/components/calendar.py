from datetime import datetime, timedelta
import discord
import calendar
from typing import Optional

class CalendarView(discord.ui.View):
    def __init__(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        callback: Optional[callable] = None,
    ):
        super().__init__(timeout = 300)
        
        now = datetime.now()
        
        deadline = now + timedelta(days=7)
        
        self.year = year or deadline.year
        self.month = month or deadline.month
        self.day = day or deadline.day
        self.selected_date = None
        self.callback = callback
            
        self._build_calendar()
        
    def _build_calendar(self):
        self.clear_items()
        
        # 月移動ボタンを直接追加
        prev_button = discord.ui.Button(label="◀ 前月", style=discord.ButtonStyle.secondary)
        current_button = discord.ui.Button(label="今月", style=discord.ButtonStyle.primary)
        next_button = discord.ui.Button(label="次月 ▶", style=discord.ButtonStyle.secondary)
        
        prev_button.callback = self._previous_month
        current_button.callback = self._current_month
        next_button.callback = self._next_month
        
        self.add_item(prev_button)
        self.add_item(current_button)
        self.add_item(next_button)
        
        # 曜日ヘッダーを追加
        weekdays = ["月", "火", "水", "木", "金", "土", "日"]
        for day in weekdays:
            header_button = discord.ui.Button(
                label=day,
                style=discord.ButtonStyle.gray,
                disabled=True
            )
            self.add_item(header_button)
        
        # カレンダーの日付ボタンを追加
        cal = calendar.monthcalendar(self.year, self.month)
        for week in cal:
            for day in week:
                if day == 0:
                    empty_button = discord.ui.Button(
                        label=" ",
                        style=discord.ButtonStyle.gray,
                        disabled=True
                    )
                    self.add_item(empty_button)
                else:
                    self.add_item(DayButton(day, self.year, self.month, callback=self.callback))
    
    async def _previous_month(self, interaction: discord.Interaction):
        """前月に移動"""
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        await self.update_calendar(interaction)
    
    async def _current_month(self, interaction: discord.Interaction):
        """今月に移動"""
        now = datetime.now()
        self.year = now.year
        self.month = now.month
        await self.update_calendar(interaction)
    
    async def _next_month(self, interaction: discord.Interaction):
        """次月に移動"""
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        await self.update_calendar(interaction)
                    
    async def update_calendar(self, interaction: discord.Interaction):
        """カレンダーを更新する"""
        self._build_calendar()
        embed = self._create_calendar_embed()
        await interaction.response.edit_message(embed=embed, view=self)
        
    def _create_calendar_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=f"📅 {self.year}年 {self.month}月",
            description="日付を選択してください",
            color=0x00ff00
        )
        
        if self.selected_date:
            embed.add_field(
                name="選択された日付",
                value=self.selected_date.strftime("%Y年%m月%d日"),
                inline=False
            )
        
        return embed


class DayButton(discord.ui.Button):
    """日付選択ボタン"""
    
    def __init__(self, day: int, year: int, month: int, callback=None):
        self.day = day
        self.year = year
        self.month = month
        self.external_callback = callback
        
        # 今日の日付をハイライト
        today = datetime.now().date()
        selected_date = datetime(year, month, day).date()
        
        if selected_date == today:
            style = discord.ButtonStyle.success
        elif selected_date < today:
            style = discord.ButtonStyle.gray
        else:
            style = discord.ButtonStyle.secondary
        
        super().__init__(
            label=str(day),
            style=style,
            disabled=(selected_date < today)  # 過去の日付は無効化
        )
    
    async def callback(self, interaction: discord.Interaction):
        selected_date = datetime(self.year, self.month, self.day)
        
        # 時間選択画面に移行
        time_view = TimeSelectionView(selected_date, self.external_callback)
        embed = time_view.create_time_embed()
        
        await interaction.response.edit_message(embed=embed, view=time_view)


class TimeSelectionView(discord.ui.View):
    """時間選択UI"""
    
    def __init__(self, selected_date: datetime, callback=None):
        super().__init__(timeout=300)
        self.selected_date = selected_date
        self.selected_hour = 23
        self.selected_minute = 59
        self.callback = callback
    
    def create_time_embed(self) -> discord.Embed:
        """時間選択のEmbedを作成"""
        embed = discord.Embed(
            title="🕐 締切時間を選択",
            description=f"**選択された日付:** {self.selected_date.strftime('%Y年%m月%d日')}\n"
                       f"**現在の時間:** {self.selected_hour:02d}:{self.selected_minute:02d}",
            color=0x00ff00
        )
        return embed
    
    @discord.ui.select(
        placeholder="時間を選択",
        options=[
            discord.SelectOption(label=f"{hour:02d}時", value=str(hour))
            for hour in range(24)
        ]
    )
    async def hour_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.selected_hour = int(select.values[0])
        embed = self.create_time_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.select(
        placeholder="分を選択",
        options=[
            discord.SelectOption(label=f"{minute:02d}分", value=str(minute))
            for minute in [0, 15, 30, 45, 59]
        ]
    )
    async def minute_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.selected_minute = int(select.values[0])
        embed = self.create_time_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="確定", style=discord.ButtonStyle.success)
    async def confirm_datetime(self, interaction: discord.Interaction, button: discord.ui.Button):
        final_datetime = self.selected_date.replace(
            hour=self.selected_hour,
            minute=self.selected_minute,
            second=0,
            microsecond=0
        )
        
        if self.callback:
            await self.callback(interaction, final_datetime)
        else:
            await interaction.response.send_message(
                f"✅ 選択された締切: {final_datetime.strftime('%Y年%m月%d日 %H:%M')}",
                ephemeral=True
            )
    
    @discord.ui.button(label="戻る", style=discord.ButtonStyle.gray)
    async def back_to_calendar(self, interaction: discord.Interaction, button: discord.ui.Button):
        calendar_view = CalendarView(
            self.selected_date.year,
            self.selected_date.month,
            callback=self.callback
        )
        embed = calendar_view._create_calendar_embed()
        await interaction.response.edit_message(embed=embed, view=calendar_view)
