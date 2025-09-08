import asyncio
import discord
from discord.ext import commands, tasks

from src.bot.commands.add import Add
from src.bot.commands.done import DoneView
from src.bot.commands.list import create_task_list
from src.database.operations import DB_Check_Pending
from src.notifications.scheduler import check_and_send_notification, start_class_end_notification_scheduler
from src.notifications.daily_due_check import start_daily_due_prompt_scheduler, run_daily_due_prompt_now
from src.config.constants import DISCORD_TOKEN, CHANNEL_ID

if not DISCORD_TOKEN and not CHANNEL_ID:
    raise ValueError("DISCORD_TOKEN または CHANNEL_ID が設定されていません")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN が設定されていません")

if not CHANNEL_ID:
    raise ValueError("CHANNEL_ID が設定されていません")


class MyClient(commands.Bot):
    def __init__(self, command_prefix='!', intents=None):
        self.discord_token = DISCORD_TOKEN
        self.channel_id = CHANNEL_ID
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(command_prefix, intents=intents)
        
    async def on_ready(self) -> None:
        print(f'{self.user} としてDiscordに接続しました!') 
        
        await self.tree.sync()
        assert CHANNEL_ID is not None
        channel = self.get_channel(int(CHANNEL_ID))
        if channel is None:
            try:
                channel = await self.fetch_channel(int(CHANNEL_ID))
                print(f"on_ready: fetch_channelでチャンネル取得成功: {CHANNEL_ID}")
            except Exception as e:
                print(f"on_ready: チャンネル取得失敗（get_channel=None, fetch_channel失敗）: id={CHANNEL_ID}, error={e}")
        if channel and hasattr(channel, "send"):
            try:
                await channel.send("Botが起動しました!")
            except Exception as e:
                print(f"on_ready: 起動メッセージ送信失敗: {e}")
        else:
            print(f"on_ready: チャンネル {self.channel_id} が見つからないか送信非対応です。設定を確認してください。")
    
        asyncio.create_task(start_class_end_notification_scheduler(self))
        # 21:00に今日締切の課題完了確認を促すスケジューラー
        asyncio.create_task(start_daily_due_prompt_scheduler(self))     
            
        if not self.notification_loop.is_running():
            self.notification_loop.start()
        
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return
        
        print(f'{message.author} からメッセージを受信しました: {message.content}')
        
    @tasks.loop(seconds=60)
    async def notification_loop(self):
        """定期的に通知をチェックし、必要な場合は送信する"""
        await check_and_send_notification(self, int(CHANNEL_ID))
        
    def run_bot(self) -> None:
        assert self.discord_token is not None
        self.run(self.discord_token)
        
def MakeClient() -> MyClient:
    client = MyClient()
    
    @client.tree.command(name="add", description="課題追加")
    async def modal_command(interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(Add())
        
    @client.tree.command(name="list", description="課題一覧を表示")
    async def list_command(interaction: discord.Interaction) -> None:
        embed = create_task_list()
        await interaction.response.send_message(embed=embed)

    @client.tree.command(name="done", description="未完了の課題を完了にする")
    async def done_command(interaction: discord.Interaction):
        tasks = DB_Check_Pending()
        if not tasks:
            await interaction.response.send_message(
                "課題はありません。", ephemeral=True
            )
            return

        embed = discord.Embed(title="課題一覧")
        for task in tasks:
            id, title, description, due_date, status = task
            embed.add_field(
                name=title,
                value=f"締切: {due_date} / 状態: {'完了' if status == 'completed' else '未完了'}",
                inline=False,
            )
        view = DoneView(tasks)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @client.tree.command(name="duecheck", description="今日が締切の課題の確認を即時送信する")
    async def duecheck_command(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            await run_daily_due_prompt_now(client)
            await interaction.followup.send("確認メッセージを送信しました。", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"送信に失敗しました: {e}", ephemeral=True)


    return client
