from discord.ext import commands
from discord import ui

@commands.command(name='button')
async def button_command(ctx: commands.Context):
    view = ui.View()
    button = ui.Button(label="Yes")
    view.add_item(button)
    await ctx.send(view=view)
