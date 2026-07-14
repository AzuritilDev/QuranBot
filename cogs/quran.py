import discord
from discord.ext import commands
from discord import app_commands
from utils import quran_fetch, metadata_fetch

class Quran(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="quran", description="Display a Qur'ân verse.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def quran(self, interaction : discord.Interaction, chapter : int, verse : int, hide_response : bool = False):
        try:
            embed = discord.Embed(title=f"Qur'ân {metadata_fetch.QuranMetadata(chapter)}, Reference: {chapter}:{verse}", description=quran_fetch.fetch(chapter, verse), color=self.bot.signature_color)
            embed.set_footer(text="(Sahîh International English Translation)", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=hide_response)
        except Exception as e:
            await interaction.response.send_message(f"```\n Error. Requested verse may not exist in the database.\n```", hide_response)
            print(e)
       

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Quran(bot))