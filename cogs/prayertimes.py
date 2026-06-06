import discord
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from adhanpy.util.DateComponents import DateComponents
from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.CalculationParameters import CalculationParameters
from adhanpy.calculation.HighLatitudeRule import HighLatitudeRule
from adhanpy.calculation.Madhab import Madhab
from adhanpy.PrayerTimes import PrayerTimes
from zoneinfo import ZoneInfo
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from timezonefinder import TimezoneFinder
import traceback

USER_AGENT = "QuranBot"

geolocator = Nominatim(user_agent=USER_AGENT)
tf = TimezoneFinder()

def get_city_coordinates(theCity: str):
    clean_input = theCity.strip()
    
    if not clean_input:
        return {"error": "Input cannot be empty."}

    try:
        location = geolocator.geocode(clean_input, featuretype="settlement", addressdetails=True)
        
        if not location:
            return {"error": f"'{clean_input}' could not be resolved to a known location."}

        raw_data = location.raw
        place_type = raw_data.get("type", "")
        valid_types = ["city", "town", "village", "administrative"]
        
        if place_type not in valid_types:
            return {"error": f"'{clean_input}' points to a {place_type}, not a valid city."}
            
        # Success path
        return {
            "latitude": location.latitude,
            "longitude": location.longitude
        }

    # Handle network and API exceptions gracefully
    except GeocoderTimedOut:
        return {"error": "The geocoding service timed out. Please try again."}
    except GeocoderServiceError as e:
        return {"error": f"Geocoding service issue ({e})."}

def fetchTzString(city : str):
    location = get_city_coordinates(city)

    if location:
        lat, lng = location["latitude"], location["longitude"]
        
        tz_string = tf.timezone_at(lng=lng, lat=lat)
        # print(f"ZoneInfo String: {tz_string}")

        local_tz = ZoneInfo(tz_string)
        return location, tz_string
        # print(f"Active ZoneInfo object: {local_tz}")
    else:
        print("Location not found.")

def fetchPrayerTimes(year : int, month : int, day : int, city : str, method : CalculationMethod, madhab : Madhab):
    date = DateComponents(year, month, day)
    params = CalculationParameters(method=method)

    # CRITICAL: Force a high latitude rule to prevent None values during summer/extreme zones
    params.high_latitude_rule = HighLatitudeRule.TWILIGHT_ANGLE

    params.madhab = madhab
    location, local_tz = fetchTzString(city)
    coordinates = (float(location["latitude"]), float(location["longitude"]))
    prayer_times = PrayerTimes(coordinates, date, calculation_parameters=params)

    return {"prayer_times": prayer_times, "local_tz": local_tz}


class PrayerTime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="prayer-times", description="Display prayer times based on given user input.")
    async def prayertime(self, interaction: discord.Interaction, city : str, method : CalculationMethod, madhab : Madhab, hide_response : bool = False):
        await interaction.response.defer(ephemeral=hide_response)
        format = "%I:%M %p"

        try:
            fetchedPrayerTimes = fetchPrayerTimes(
                datetime.today().year, 
                datetime.today().month,
                datetime.today().day,
                city,
                method,
                madhab
                )
            prayer_times = fetchedPrayerTimes["prayer_times"]

            prayers = {
                "Fajr": prayer_times.fajr,
                "Sunrise": prayer_times.sunrise,
                "Dhuhr": prayer_times.dhuhr,
                "Asr": prayer_times.asr,
                "Maghrib": prayer_times.maghrib,
                "Isha": prayer_times.isha
            }

            current_time = datetime.now(ZoneInfo("UTC"))

            next_prayer_name = None
            next_prayer_time = None

            for name, p_time in sorted(prayers.items(), key=lambda item: item[1]):
                if p_time > current_time:
                    next_prayer_name = name
                    next_prayer_time = p_time
                    break

            if not next_prayer_time:
                next_prayer_name = "Fajr (Tomorrow)"
                total_seconds = 0 
            else:
                total_seconds = int(next_prayer_time.timestamp() - current_time.timestamp())


            time_difference = next_prayer_time - current_time
            total_seconds = int(time_difference.total_seconds())

            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            if total_seconds == 0:
                countdown_text = "All of today's prayers have concluded."
            elif hours > 0:
                countdown_text = f"{hours} hour{'s' if hours > 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''} left until next prayer."
            else:
                countdown_text = f"{minutes} minute{'s' if minutes != 1 else ''} left until next prayer."

            tz = ZoneInfo(fetchedPrayerTimes["local_tz"])

            fajr = prayer_times.fajr.astimezone(tz).strftime(format)
            sunrise = prayer_times.sunrise.astimezone(tz).strftime(format)
            dhuhr = prayer_times.dhuhr.astimezone(tz).strftime(format)
            asr = prayer_times.asr.astimezone(tz).strftime(format)
            maghrib = prayer_times.maghrib.astimezone(tz).strftime(format)
            isha = prayer_times.isha.astimezone(tz).strftime(format)

            embed = discord.Embed(title="Islamic Prayer Times of Today", description=f"Current Time: {datetime.today().astimezone(tz).strftime(format)}", color=self.bot.signature_color)
            embed.set_author(name=f"Next Prayer: {next_prayer_name}")
            embed.add_field(name="Fajr", value=fajr, inline=False)
            embed.add_field(name="Sunrise", value=sunrise, inline=False)
            embed.add_field(name="Dhuhr", value=dhuhr, inline=False)
            embed.add_field(name="Asr", value=asr, inline=False)
            embed.add_field(name="Maghrib", value=maghrib, inline=False)
            embed.add_field(name="Isha", value=isha, inline=False)
            embed.set_footer(text=countdown_text)

            await interaction.followup.send(embed=embed, ephemeral=hide_response)
        except Exception as e:
            await interaction.followup.send(f"An error occured while fetching prayer times: {e} {traceback.extract_tb(e.__traceback__)}")


async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(PrayerTime(bot))