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

            try:
                start = time.perf_counter()
                async with self.bot.db_pool.acquire() as cur:
                        row = await cur.fetchrow("SELECT VERSION();")
                        split_ver_string = str(row[0]).split(" ")
                        version = f"{split_ver_string[0]} {split_ver_string[1]}"
                ping = (time.perf_counter() - start) * 1000
                db_status = f"✅ Connected (`{int(ping)} ms`)"
            except Exception as e:
                version = "N/A"
                db_status = f"❌ Disconnected ({type(e).__name__})"

            embed.set_thumbnail(url=self.bot.user.avatar.url)

            embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)} ms")
            embed.add_field(name="Python Version", value=platform.python_version())
            embed.add_field(name="discord.py Version", value=discord.__version__)
            embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%")
            embed.add_field(name="RAM Usage", value=f"{psutil.virtual_memory().percent}%")
            embed.add_field(name="System", value=platform.system())

            embed.add_field(name="Database", value="PostgreSQL")
            embed.add_field(name="Database Version", value=version)
            embed.add_field(name="Database Status", value=db_status)

            embed.set_footer(text=f"System Uptime: {round(uptime / 3600, 2)} hours\nBot Uptime: {uptime_str}\nGitHub Repository: https://github.com/AzuritilDev/QuranBot", icon_url=self.bot.user.avatar.url)
            
            await interaction.followup.send(embed=embed, ephemeral=hide_response)
        except Exception as e:
            print("Status Debug: ", e)

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Status(bot))