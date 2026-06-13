import discord
import datetime
import random
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo
from utils.quran_fetch import any_fetch
from utils.quotables import quotable_verses

class VerseLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 1. Start the loop right when the Cog loads
        self.daily_quran_task.start()

    @tasks.loop(minutes=1)
    async def daily_quran_task(self):
        # Now safe: Database pool is guaranteed to be ready here
        async with self.bot.db_pool.acquire() as cur:
            rows = await cur.fetch("""
                SELECT *
                FROM dailyquran
            """)

        # Using datetime.now(tz) is the modern, non-deprecated way in Python 3.12+
        utc_now = datetime.datetime.now(ZoneInfo("UTC"))

        for row in rows:
            try:
                tz = ZoneInfo(row["timezone"])
                local_time = utc_now.astimezone(tz)

                # send every day at 09:00 local time
                if local_time.hour != 9 or local_time.minute != 0:
                    continue

                today = local_time.date()

                # already sent today
                if row["last_sent_date"] == today:
                    continue

                try:
                    webhook = await self.bot.fetch_webhook(
                        row["webhook_id"]
                    )

                except discord.NotFound:
                    # webhook deleted manually
                    async with self.bot.db_pool.acquire() as cur:
                        await cur.execute(
                            """
                            DELETE FROM dailyquran
                            WHERE guild_id = $1
                            """,
                            row["guild_id"]
                        )
                    continue

                selected_verse = random.choice(quotable_verses)
                verse_contents, verse_reference = any_fetch(selected_verse)

                verse_text = (
                    f"{verse_contents}\n"
                    f"— Qur'ân {verse_reference}"
                )

                await webhook.send(verse_text)

                async with self.bot.db_pool.acquire() as cur:
                    await cur.execute(
                        """
                        UPDATE dailyquran
                        SET last_sent_date = $1
                        WHERE guild_id = $2
                        """,
                        today,
                        row["guild_id"]
                    )

            except Exception as e:
                print(
                    f"Failed daily Quran task for guild "
                    f"{row['guild_id']}: {e}"
                )
    
    @daily_quran_task.before_loop
    async def before_daily_quran_task(self):
        # 1. Wait for Discord to be fully ready
        await self.bot.wait_until_ready()
        
        # 2. Wait until the bot actually creates the DB pool attribute
        while not hasattr(self.bot, 'db_pool') or self.bot.db_pool is None:
            await discord.utils.sleep_until(datetime.datetime.now() + datetime.timedelta(seconds=1))
    
    def cog_unload(self):
        self.daily_quran_task.cancel()

async def setup(bot):
    await bot.add_cog(VerseLoop(bot))
