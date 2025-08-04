import discord
from src.database.operations import DB_Check_Pending


def create_task_list() -> discord.Embed:
    tasks = DB_Check_Pending()

    embed = discord.Embed(title="課題一覧", color=discord.Color.blue())

    if not tasks:
        embed.description = "現在、登録されている課題はありません。"
        return embed

    for task in tasks:
        id, title, description, due_date, status = task

        emoji = "✅" if status == "completed" else "❌"

        embed.add_field(
            name=f"{title} {emoji}",
            value=f"締切: {due_date},\n説明:{description}",
            inline=False,
        )

    return embed
