import discord
from discord.ext import commands
from discord import app_commands
import adhanpy

class PrayerTimes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="prayer-times", description="Display prayer times based on given user input.")
    async def prayertimes(self, interaction: discord.Interaction, hide_response : bool = False):
        pass

async def PrayerTimes(bot : commands.Bot) -> None:
    await bot.add_cog(PrayerTimes(bot))