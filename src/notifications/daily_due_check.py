import asyncio
from datetime import datetime
from typing import Optional

import discord

from src.bot.commands.done import DoneView
from src.database.operations import DB_Check_Pending
from src.config.constants import CHANNEL_ID, DAILY_DUE_PROMPT_HOUR, DAILY_DUE_PROMPT_MINUTE


# その日のリマインド実行を一度に制限するための記録
_last_prompt_date: Optional[str] = None


async def _send_today_due_prompt(client: discord.Client) -> None:
    """今日が締切の未完了タスクについて、完了確認を促すメッセージを送信する。"""
    channel_id_str = CHANNEL_ID
    if not channel_id_str:
        print("CHANNEL_IDが設定されていません。")
        return

    try:
        channel_id = int(channel_id_str)
    except ValueError:
        print(f"CHANNEL_IDが無効な値です: {channel_id_str}")
        return

    channel = client.get_channel(channel_id)
    if not channel or not hasattr(channel, "send"):
        print(f"チャンネルID {channel_id} が見つからないか、送信不可です。")
        return

    # DBから未完了タスクを取得し、今日締切のみに絞る
    pending_tasks = DB_Check_Pending()
    today_prefix = datetime.now().strftime("%m/%d")  # due_date は "MM/DD HH:MM" 形式
    todays_tasks = [t for t in pending_tasks if isinstance(t[3], str) and t[3].startswith(today_prefix)]

    if not todays_tasks:
        # 今日締切の未完了タスクがない場合は完了メッセージを送信
        try:
            await channel.send("本日のタスクはすべて完了しています！")
        except Exception as e:
            print(f"21時完了メッセージ送信エラー: {e}")
        return

    embed = discord.Embed(
        title="今日が期日の課題の確認",
        description="21:00です。以下の課題は完了しましたか？",
        color=0xFFA500,
        timestamp=datetime.now(),
    )
    for task in todays_tasks:
        _id, title, _desc, due_date, _status = task
        embed.add_field(name=title, value=f"締切: {due_date}", inline=False)

    view = DoneView(todays_tasks)

    try:
        await channel.send(embed=embed, view=view)
    except Exception as e:
        print(f"21時確認メッセージ送信エラー: {e}")


async def start_daily_due_prompt_scheduler(client: discord.Client) -> None:
    """
    毎日21:00に、当日締切のタスクが完了したかを確認するメッセージを送信するスケジューラ。
    - 21:00以降その日のうちに一度だけ通知する。
    - due_date は "MM/DD HH:MM" 形式を想定。
    """
    global _last_prompt_date
    print("21時のデイリー課題確認スケジューラーを開始します...")

    while True:
        try:
            now = datetime.now()
            today = now.strftime("%Y-%m-%d")
            target = now.replace(
                hour=DAILY_DUE_PROMPT_HOUR,
                minute=DAILY_DUE_PROMPT_MINUTE,
                second=0,
                microsecond=0,
            )

            # 21:00以降、かつ未送信なら送る（ループの取りこぼし対策）
            if now >= target and _last_prompt_date != today:
                await _send_today_due_prompt(client)
                _last_prompt_date = today
        except Exception as e:
            print(f"デイリープロンプト実行中にエラー: {e}")

        # 1分ごとにチェック
        await asyncio.sleep(60)
