import discord
from datetime import datetime, timedelta
from discord.ext import commands
from discord import app_commands
from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.Madhab import Madhab
from zoneinfo import ZoneInfo
from utils.geography import fetchPrayerTimes, availableTimeFormats
from utils.beautify import beautifyCalculationMethodClassName

class PrayerTime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="prayer-times", description="Display prayer times based on given user input.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    @app_commands.describe(city="Times given according to which city?")
    @app_commands.describe(time_format="The time format, whether you want a 24-hour military time based output (Example: 18:30) or a 12-hour time output (Example: 6:30 PM). Default is 24-hour military time.")
    @app_commands.describe(method="Based on which calculation method, default is Moon Sighting Committee.")
    @app_commands.describe(madhab="The Asr calculation method. Default is Hanafi.")
    @app_commands.describe(display_city_name="Whether you want to display the name of the city selected or not. Default is True.")
    @app_commands.describe(times_inline="Whether you want the times inside the embed to be inline or not. Default is True.")
    async def prayertime(self, interaction: discord.Interaction, city : str, time_format : availableTimeFormats = availableTimeFormats.TWENTY_FOUR_HOUR_MILITARY_TIME, method : CalculationMethod = CalculationMethod.MOON_SIGHTING_COMMITTEE, madhab : Madhab = Madhab.HANAFI, display_city_name : bool = True, times_inline : bool = True, hide_response : bool = False):
        if len(city) > 170:
            await interaction.response.send_message("City name is too long.")
            return
        
        await interaction.response.defer(ephemeral=hide_response)
        used_format = time_format.value

        try:
            fetchedPrayerTimes = await fetchPrayerTimes(
                datetime.today().year, 
                datetime.today().month,
                datetime.today().day,
                city,
                method,
                madhab
                )
            
            if "error" in fetchedPrayerTimes:
                await interaction.followup.send(f"# Error\n{fetchedPrayerTimes['error']}", ephemeral=hide_response)
                return

            prayer_times = fetchedPrayerTimes["prayer_times"]
            tz = ZoneInfo(fetchedPrayerTimes["local_tz"])
        except Exception as e:
            await interaction.followup.send(f"An error occured while fetching prayer times: {e}")
            return
        
        try:
            prayers = {
                "Fajr": prayer_times.fajr.replace(tzinfo=tz),
                "Sunrise": prayer_times.sunrise.replace(tzinfo=tz),
                "Dhuhr": prayer_times.dhuhr.replace(tzinfo=tz),
                "Asr": prayer_times.asr.replace(tzinfo=tz),
                "Maghrib": prayer_times.maghrib.replace(tzinfo=tz),
                "Isha": prayer_times.isha.replace(tzinfo=tz)
            }
            print(prayers)

            current_time = datetime.now(tz)

            next_prayer_name = None
            next_prayer_time = None

            for name, p_time in sorted(prayers.items(), key=lambda item: item[1]):
                if p_time and p_time > current_time:
                    next_prayer_name = name
                    next_prayer_time = p_time
                    break


            if next_prayer_time is None:
                today_or_tmrw = "Tomorrow"
                next_prayer_name = "Fajr (Tomorrow)"

                # fetch tomorrow's prayer times
                tomorrow = datetime.now(tz) + timedelta(days=1)

                tomorrow_prayers = await fetchPrayerTimes(
                    tomorrow.year,
                    tomorrow.month,
                    tomorrow.day,
                    city,
                    method,
                    madhab
                )

                next_prayer_time = tomorrow_prayers["prayer_times"].fajr.astimezone(tz)
            else:
                today_or_tmrw = "Today"

            time_difference = next_prayer_time - current_time
            total_seconds = int(time_difference.total_seconds())

            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            if total_seconds <= 0:
                countdown_text = "All of today's prayers have concluded."
            elif hours > 0:
                countdown_text = f"{hours} hour{'s' if hours > 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''} left until next prayer."
            else:
                countdown_text = f"{minutes} minute{'s' if minutes != 1 else ''} left until next prayer."

            tz = ZoneInfo(fetchedPrayerTimes["local_tz"])

            fajr = prayer_times.fajr.astimezone(tz).strftime(used_format)
            sunrise = prayer_times.sunrise.astimezone(tz).strftime(used_format)
            dhuhr = prayer_times.dhuhr.astimezone(tz).strftime(used_format)
            asr = prayer_times.asr.astimezone(tz).strftime(used_format)
            maghrib = prayer_times.maghrib.astimezone(tz).strftime(used_format)
            isha = prayer_times.isha.astimezone(tz).strftime(used_format)

            safe_city_name = discord.utils.escape_markdown(city)
            embed_title = f"City: {safe_city_name}\nIslamic Prayer Times of {today_or_tmrw}" if display_city_name else f"Islamic Prayer Times of {today_or_tmrw}"

            embed = discord.Embed(title=embed_title, description=f"Current Time: {datetime.today().astimezone(tz).strftime(used_format)}", color=self.bot.signature_color)
            embed.set_author(name=f"Next Prayer: {next_prayer_name}")
            embed.add_field(name="Fajr", value=fajr, inline=times_inline)
            embed.add_field(name="Sunrise", value=sunrise, inline=times_inline)
            embed.add_field(name="Dhuhr", value=dhuhr, inline=times_inline)
            embed.add_field(name="Asr", value=asr, inline=times_inline)
            embed.add_field(name="Maghrib", value=maghrib, inline=times_inline)
            embed.add_field(name="Isha", value=isha, inline=times_inline)
            embed.set_footer(text=f"{countdown_text}\n\nCalculation Method: {beautifyCalculationMethodClassName(method.name)}\nAsr Method: {beautifyCalculationMethodClassName(madhab.name)}", icon_url=self.bot.user.avatar.url)

            await interaction.followup.send(embed=embed, ephemeral=hide_response)
        except Exception as e:
            await interaction.followup.send(f"Something happend while trying to display prayer times.\n\nError message:\n```bash\n{e}\n```")


async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(PrayerTime(bot))