import discord
from discord.ext import commands
from discord import app_commands
import asyncpg

DEFAULT_WEBHOOK_NAME = "Automatic Daily Qur'ân Verses"

async def webhookWithExpectedNameAlreadyExists(channel : discord.TextChannel):
    webhooks = await channel.webhooks()
    target = discord.utils.get(webhooks, name=DEFAULT_WEBHOOK_NAME)
    return target is None
        
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

def timezoneIsValid(tz_string):
    try:
        ZoneInfo(tz_string)
        return True
    except (ZoneInfoNotFoundError, ValueError):
        # ValueError may be raised for non-conforming keys (e.g., up-level references)
        return False

class setDailyQuran(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="set-daily-quran", description="Set a channel to display daily Qur'ân verses in.")
    @app_commands.default_permissions(manage_channels=True)
    async def set_daily_quran(self, interaction : discord.Interaction, channel : discord.TextChannel, timezone : str, hide_response : bool = False):
        # check user permissions before complying
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("You need to have the `Manage Channels` guild permission in order to run this command.", ephemeral=hide_response)
            return
        # database queries may take time to finish
        await interaction.response.defer(ephemeral=hide_response)

        # create the table for Daily Quran channels if it does not exist and check if the guild already has a notifier
        async with self.bot.db_pool.acquire() as cur:
            row = await cur.fetchrow("""SELECT * FROM dailyquran WHERE guild_id = $1;""", interaction.guild_id)
            if row:
                try:
                    webhook = await self.bot.fetch_webhook(row["webhook_id"])

                    # webhook still exists
                    await interaction.followup.send(
                        f"This server already has a notifier in <#{row['channel_id']}>."
                    )
                    return

                except discord.NotFound:
                    # webhook deleted manually
                    async with self.bot.db_pool.acquire() as cur:
                        await cur.execute(
                            "DELETE FROM dailyquran WHERE guild_id = $1",
                            interaction.guild_id
                        )

                except discord.Forbidden:
                    await interaction.followup.send(
                        "I no longer have access to the existing webhook."
                    )
                    return

        criteria1 = await webhookWithExpectedNameAlreadyExists(channel)
        criteria2 = timezoneIsValid(timezone)

        if criteria1:
            await interaction.followup.send(f"There is already a webhook in <#{channel.id}> named '{DEFAULT_WEBHOOK_NAME}'.\n\nEither delete it or change its name from the channel's settings.")
            return
        
        if not criteria2:
            await interaction.followup.send("Timezone is not valid.\n\nThe valid format should look something like `Area/Location`.\nExamples:\n```America/New_York\nEurope/London\nAsia/Tokyo\nAustralia/Sydney```\n\nPlease check [IANA Time Zone Database](https://www.iana.org/time-zones) and [List of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) for more info.\nThis bot uses Python's ZoneInfo module, also the input may be case-sensetive.")
            return

        bot_permissions = channel.permissions_for(interaction.guild.me)

        missing_permissions = []

        if not bot_permissions.view_channel:
            missing_permissions.append("View Channel")

        if not bot_permissions.manage_webhooks:
            missing_permissions.append("Manage Webhooks")

        if missing_permissions:
            await interaction.followup.send(
                "I am missing the following permissions in that channel:\n- "
                + "\n- ".join(missing_permissions)
            )
            return

        avatar_bytes = await self.bot.user.display_avatar.read()
        try:
            new_webhook = await channel.create_webhook(name=DEFAULT_WEBHOOK_NAME, avatar=avatar_bytes)
        except discord.Forbidden:
            await interaction.followup.send("A problem occurred while creating the webhook.\n\nTry again later.")
            return

        try:
            async with self.bot.db_pool.acquire() as cur:
                await cur.execute("""INSERT INTO dailyquran (channel_id, guild_id, webhook_id, timezone) 
                                VALUES ($1, $2, $3, $4)
                                ON CONFLICT (guild_id)
                                DO UPDATE SET
                                    channel_id = EXCLUDED.channel_id,
                                    webhook_id = EXCLUDED.webhook_id,
                                    timezone = EXCLUDED.timezone;""", channel.id, interaction.guild_id, new_webhook.id, timezone)
        except Exception:
            await new_webhook.delete(reason="Database insert failed")
            raise

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(setDailyQuran(bot))