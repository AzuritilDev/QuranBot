import time
import psutil
import platform
import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="status", description="Shows system information about the bot.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def status(self, interaction : discord.Interaction, hide_response : bool = False):
        await interaction.response.defer(ephemeral=hide_response)
        try:
            uptime = time.time() - psutil.boot_time()
            embed = discord.Embed(title="Bot Status", color=self.bot.signature_color)
            now = time.time()
            uptime_seconds = int(now - self.bot.launch_time)
            uptime_str = str(timedelta(seconds=uptime_seconds))

            # for PostgreSQL
            try:
                start = time.perf_counter()
                async with self.bot.db_pool.acquire() as cur:
                        row = await cur.fetchrow("SELECT VERSION();")
                        split_ver_string = str(row[0]).split(" ")
                        version = f"{split_ver_string[1]}"
                ping = (time.perf_counter() - start) * 1000
                if ping > 100:
                    db_status = f"⚠️ Connected (`{int(ping)} ms`) [Abnormally Slow]"
                else:
                    db_status = f"✅ Connected (`{int(ping)} ms`) [Healthy]"
            except Exception as e:
                version = "N/A"
                db_status = f"❌ Disconnected ({type(e).__name__})"

            # for Redis
            try:
                start_2 = time.perf_counter()

                redis_is_connected = await self.bot.redis.ping()
                if redis_is_connected:
                    redis_latency = (time.perf_counter() - start_2) * 1000
                
                    if redis_latency > 5:
                        redis_status = f"⚠️ Connected (`{int(redis_latency)} ms`) [Abnormally Slow]"
                    else:
                        redis_status = f"✅ Connected (`{int(redis_latency)} ms`) [Healthy]"

                    redis_info = await self.bot.redis.info()
                    redis_version = redis_info["redis_version"]
            except Exception as e:
                redis_version = "N/A"
                redis_status = f"❌ Disconnected ({type(e).__name__})"

            embed.set_thumbnail(url=self.bot.user.avatar.url)

            embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)} ms")
            embed.add_field(name="Python Version", value=platform.python_version())
            embed.add_field(name="discord.py Version", value=discord.__version__)
            embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%")
            embed.add_field(name="RAM Usage", value=f"{psutil.virtual_memory().percent}%")
            embed.add_field(name="System", value=platform.system())

            # Relational DB
            embed.add_field(name="Relational Database", value="PostgreSQL")
            embed.add_field(name="Relational Database Version", value=version)
            embed.add_field(name="Relational Database Status", value=db_status)

            # In-Memory DB
            embed.add_field(name="In-Memory Database", value="Redis")
            embed.add_field(name="In-Memory Database Version", value=redis_version)
            embed.add_field(name="In-Memory Database Status", value=redis_status)

            embed.set_footer(text=f"System Uptime: {round(uptime / 3600, 2)} hours\nBot Uptime: {uptime_str}\nGitHub Repository: https://github.com/AzuritilDev/QuranBot", icon_url=self.bot.user.avatar.url)
            
            await interaction.followup.send(embed=embed, ephemeral=hide_response)
        except Exception as e:
            print("Status Debug: ", e)

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Status(bot))