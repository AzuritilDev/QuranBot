import discord
from discord.ext import commands
from discord import app_commands

class Hadith(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hadith", description="Displays a narration.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def hadith(self, interaction: discord.Interaction, hide_response : bool = False):
        pass

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Hadith(bot))