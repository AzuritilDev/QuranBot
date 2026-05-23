import discord
from discord.ext import commands
from discord import app_commands
import asyncpg

async def webhookWithExpectedNameAlreadyExists(interaction:  discord.Interaction):
    webhooks = await interaction.channel.webhooks()
    target = discord.utils.get(webhooks, name="Daily Quran Verses")
    if target:
        return True

async def theGuildAlreadyHasAWebhookInRecords(interaction : discord.Interaction, db_pool : asyncpg.Pool):
    async with db_pool.acquire() as cur:
        row = await cur.fetchrow("""SELECT * FROM dailyquran
                                WHERE channel_id = $1""", interaction.channel_id)
        if row != None:
            return True

class setDailyQuran(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="set-daily-quran", description="Set a channel to display daily Qur'ân verses in.")
    async def set_daily_quran(self, interaction : discord.Interaction, hide_response : bool = False):
        if not interaction.user.guild_permissions.manage_channels:
            interaction.response.send_message("You need to have the `Manage Channels` guild permission in order to run this command.", ephemeral=hide_response)
            return
        await interaction.response.defer(ephemeral=hide_response)

        async with self.bot.db_pool.acquire() as cur:
            await cur.execute("""CREATE TABLE IF NOT EXISTS dailyquran (channel_id BIGINT PRIMARY KEY)""")

        criteria1 = webhookWithExpectedNameAlreadyExists(interaction)
        criteria2 = theGuildAlreadyHasAWebhookInRecords(interaction, self.bot.db_pool)

        if not (criteria1 and criteria2) == False:
            async with self.bot.db_pool.acquire() as cur:
                await cur.execute("""INSERT INTO dailyquran ()""")
                # WIP

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(setDailyQuran(bot))