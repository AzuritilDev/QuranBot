import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show all available commands and usage.")
    async def help(self, interaction: discord.Interaction, hide_response : bool = False):
        embed = discord.Embed(
            title="📘 Help - Command List",
            color=discord.Color.red()
        )
        # available commands
        embed.add_field(name="/help", value="(Lists all the available slash commands of the bot.).", inline=False)

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Help(bot))