import asyncio
import os
from datetime import datetime

import discord

from src.bot.commands.add import Add
from src.data.date_utils import GetWeek, get_subject_by_period
from src.data.read_json import read_json

# 通知済みの授業を記録するセット（日付-時限で管理）
notified_classes = set()
last_cleared_date = None


class TaskAddView(discord.ui.View):
    """課題追加確認用のビュー"""

    def __init__(self, task_title: str):
        super().__init__(timeout=300)
        self.task_title = task_title

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success, emoji="✅")
    async def yes_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Yesボタンが押されたときの処理"""
        await interaction.response.send_modal(Add(subject_name=self.task_title))

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger, emoji="❌")
    async def no_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Noボタンが押されたときの処理"""
        await interaction.response.send_message(
            "課題追加をキャンセルしました。", ephemeral=True
        )
        self.stop()


async def send_class_and_notification(client: discord.Client, task_title: str):
    """
    課題追加の確認メッセージを送信し、ユーザーの応答を待つ
    Args:
        client (discord.Client): Discordクライアント
        task_title (str): 課題のタイトル
    """
    channel_id_str = os.getenv("CHANNEL_ID")
    if not channel_id_str:
        print("CHANNEL_IDが設定されていません。")
        return

    try:
        channel_id = int(channel_id_str)
    except ValueError:
        print(f"CHANNEL_IDが無効な値です: {channel_id_str}")
        return

    channel = client.get_channel(channel_id)

    if not channel:
        print(f"チャンネルID {channel_id} が見つかりません。")
        return

    # チャンネルタイプのチェック
    if not hasattr(channel, "send"):
        print(f"チャンネル {channel_id} はメッセージ送信に対応していません。")
        return

    embed = discord.Embed(
        title="授業完了通知",
        description=f"**{task_title}** の授業が終了しました!",
        color=0x00FF00,
        timestamp=datetime.now(),
    )
    embed.add_field(
        name="課題追加", value=f"{task_title} の課題を追加しますか？", inline=False
    )

    view = TaskAddView(task_title)

    try:
        await channel.send(embed=embed, view=view)
    except Exception as e:
        print(f"メッセージ送信エラー: {e}")


async def check_and_send_notification(client: discord.Client, channel_id: int):
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_weekday = GetWeek()
    today_str = now.strftime("%Y-%m-%d")

    timetable = read_json("dataset/timetable.json")
    period_data = read_json("dataset/period.json")

    if not timetable or not period_data:
        print("タイムテーブルまたは期間データが読み込めませんでした。")
        return

    for period_num in range(1, 6):  # 1〜5限まで
        period_str = str(period_num)
        if period_str not in period_data:
            continue

        end_time = period_data[period_str]["end_time"]
        notification_key = f"{today_str}_{period_str}"

        # 現在時刻が終了時刻以降で、まだ通知していない場合
        if current_time >= end_time and notification_key not in notified_classes:
            subject_name = get_subject_by_period(timetable, current_weekday, period_num)

            if subject_name and subject_name.strip() != "":
                await send_class_and_notification(client, subject_name)
                notified_classes.add(notification_key)

    # 日付が変わったら通知履歴をクリア
    global last_cleared_date
    current_date = now.strftime("%Y-%m-%d")
    if last_cleared_date is None:
        last_cleared_date = current_date
    elif last_cleared_date != current_date:
        notified_classes.clear()
        last_cleared_date = current_date


async def start_class_end_notification_scheduler(client: discord.Client):
    """
    授業終了通知のスケジューラーを開始
    Args:
        client (discord.Client): Discordクライアント
    """
    print("授業終了通知スケジューラーを開始します...")

    channel_id = os.getenv("CHANNEL_ID")
    if not channel_id:
        print("CHANNEL_IDが設定されていません")
        return

    # 定期的に授業終了通知をチェック
    while True:
        try:
            await check_and_send_notification(client, int(channel_id))
        except Exception as e:
            print(f"通知チェック中にエラーが発生しました: {e}")
        await asyncio.sleep(60)  # 1分ごとにチェック
