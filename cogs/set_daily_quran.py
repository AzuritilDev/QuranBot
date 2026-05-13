import discord
from discord.ext import commands
from discord import app_commands

class setDailyQuran(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="set-daily-quran", description="Set a channel to display daily Qur'ân verses in.")
    async def set_daily_quran(self, interaction: discord.Interaction, hide_response : bool = False):
        pass

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(setDailyQuran(bot))