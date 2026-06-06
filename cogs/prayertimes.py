import discord
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from adhanpy.util.DateComponents import DateComponents
from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.CalculationParameters import CalculationParameters
from adhanpy.calculation.Madhab import Madhab
from adhanpy.PrayerTimes import PrayerTimes
from zoneinfo import ZoneInfo
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from timezonefinder import TimezoneFinder

USER_AGENT = "QuranBot"

geolocator = Nominatim(user_agent=USER_AGENT)
tf = TimezoneFinder()

def get_city_coordinates(theCity : str):
    clean_input = theCity.strip()
    
    if not clean_input:
        return "Error: Input cannot be empty."

    try:
        location = geolocator.geocode(clean_input, featuretype="settlement", addressdetails=True)
        
        if not location:
            return f"Error: '{clean_input}' could not be resolved to a known location."

        raw_data = location.raw
        place_type = raw_data.get("type", "")
        valid_types = ["city", "town", "village", "administrative"]
        
        if place_type not in valid_types:
            return f"Error: '{clean_input}' points to a {place_type}, not a valid city."
            
        # Success path
        return {
            # "display_name": location.address,
            "latitude": location.latitude,
            "longitude": location.longitude,
            # "city_name": raw_data["address"].get("city") or raw_data["address"].get("town")
        }

    # Handle network and API exceptions gracefully
    except GeocoderTimedOut:
        return "Error: The geocoding service timed out. Please try again."
    except GeocoderServiceError as e:
        return f"Error: Geocoding service issue ({e})."

def fetchTzString(city : str):
    location : dict = get_city_coordinates(city)

    if location:
        lat, lng = location.latitude, location.longitude
        print(f"Coordinates: {lat}, {lng}")
        
        tz_string = tf.timezone_at(lng=lng, lat=lat)
        # print(f"ZoneInfo String: {tz_string}")

        local_tz = ZoneInfo(tz_string)
        location.update({"tz_string": local_tz})
        return location
        # print(f"Active ZoneInfo object: {local_tz}")
    else:
        print("Location not found.")

def fetchPrayerTimes(year : int, month : int, day : int, city : str, method : CalculationMethod, madhab : Madhab):
    date = DateComponents(year, month, day)
    params = CalculationParameters(method=method)
    params.madhab = madhab
    location_and_timezone = fetchTzString(city)
    coordinates = (location_and_timezone.latitude, location_and_timezone.longitude)

    prayer_times = PrayerTimes(coordinates, date, calculation_parameters=params)

    prayer_times.update({"tz_string": location_and_timezone.tz_string})
    return prayer_times


class PrayerTimes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="prayer-times", description="Display prayer times based on given user input.")
    async def prayertimes(self, interaction: discord.Interaction, city : str, method : CalculationMethod, madhab : Madhab, hide_response : bool = False):
        await interaction.response.defer(ephemeral=hide_response)
        format = "%I:%M %p"

        prayer_times = fetchPrayerTimes(
            datetime.today().year, 
            datetime.today().month,
            datetime.today().day,
            city,
            method,
            madhab
            )
        
        next_prayer_enum = prayer_times.next_prayer()
        next_prayer_time = prayer_times.time_for_prayer(next_prayer_enum)

        current_time = datetime.now(next_prayer_time.tzinfo)

        time_difference = next_prayer_time - current_time
        total_seconds = int(time_difference.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        if hours > 0:
            countdown_text = f"{hours} hour{'s' if hours > 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''} left until next prayer."
        else:
            countdown_text = f"{minutes} minute{'s' if minutes != 1 else ''} left until next prayer."

        tz = prayer_times.tz_string

        fajr = prayer_times.fajr.astimezone(tz).strftime(format)
        sunrise = prayer_times.sunrise.astimezone(tz).strftime(format)
        dhuhr = prayer_times.dhuhr.astimezone(tz).strftime(format)
        asr = prayer_times.asr.astimezone(tz).strftime(format)
        maghrib = prayer_times.maghrib.astimezone(tz).strftime(format)
        isha = prayer_times.isha.astimezone(tz).strftime(format)

        embed = discord.Embed(title="Islamic Prayer Times of Today", description=f"Current Time: {datetime.today().astimezone(tz).strftime(format)}", color=self.bot.signature_color)
        embed.set_author(f"Next Prayer: {next_prayer_enum.name}")
        embed.add_field(name="Fajr", value=fajr, inline=False)
        embed.add_field(name="Sunrise", value=sunrise, inline=False)
        embed.add_field(name="Dhuhr", value=dhuhr, inline=False)
        embed.add_field(name="Asr", value=asr, inline=False)
        embed.add_field(name="Maghrib", value=maghrib, inline=False)
        embed.add_field(name="Isha", value=isha, inline=False)
        embed.set_footer(countdown_text)

        await interaction.followup.send(embed=embed, ephemeral=hide_response)


async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(PrayerTimes(bot))