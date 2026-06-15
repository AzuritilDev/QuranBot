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
            color=self.bot.signature_color
        )
        # available commands
        embed.add_field(name="/help", value="(Lists all the available slash commands of the bot.).", inline=False)
        embed.add_field(name="/quran", value="(Displays a Qur'ân verse based on the user's input.).", inline=False)
        embed.add_field(name="/set-daily-quran", value="(Displays verses on a selected channel daily.).", inline=False)
        embed.add_field(name="/prayer-times", value="(Displays the Islamic prayer times based on selected city.).", inline=False)
        embed.add_field(name="/status", value="(Displays system information about the bot.).", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=hide_response)

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Help(bot))