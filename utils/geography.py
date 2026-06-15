import asyncio
from adhanpy.util.DateComponents import DateComponents
from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.CalculationParameters import CalculationParameters
from adhanpy.calculation.HighLatitudeRule import HighLatitudeRule
from adhanpy.calculation.Madhab import Madhab
from adhanpy.PrayerTimes import PrayerTimes
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from timezonefinder import TimezoneFinder
from enum import Enum
# from zoneinfo import ZoneInfo

# Constants, 
# if you're a developer and you're hosting your own version of the bot
# feel free to change these according to your liking
USER_AGENT = "QuranBot"
GEOPY_CLIENT_TIMEOUT = 5
GEOPY_MAXIMUM_RETRIES = 3

tf = TimezoneFinder()

class availableTimeFormats(Enum):
    TWELVE_HOUR_TIME = "%I:%M %p"
    TWENTY_FOUR_HOUR_MILITARY_TIME = "%H:%M"

async def get_city_coordinates(theCity: str, bot_geolocator : Nominatim):
    clean_input = theCity.strip()
    
    if not clean_input:
        return {"error": "Input cannot be empty."}

    for attempt in range(GEOPY_MAXIMUM_RETRIES):
        try:
            location = await bot_geolocator.geocode(
                clean_input,
                addressdetails=True
            )
            
            if not location:
                return {"error": f"'{clean_input}' could not be resolved to a known location."}

            raw_data = location.raw
            place_type = raw_data.get("addresstype", "")
            valid_types = [
                "city",
                "town",
                "village",
                "administrative",
                "municipality",
                "province",
                "state_district",
                "region",
            ]
            
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
    
async def fetchLocationAndTzString(city : str, geolocator : Nominatim):
    location = await get_city_coordinates(city, geolocator)

    if location and "error" not in location:
        lat, lng = location["latitude"], location["longitude"]
        tz_string = tf.timezone_at(lng=lng, lat=lat)
        # print(f"ZoneInfo String: {tz_string}")
        # local_tz = ZoneInfo(tz_string)
        return location, tz_string
    else:
        # Pass the actual error forward or handle it
        error_msg = location.get("error", "Location not found.") if location else "Location not found."
        print(f"Error: {error_msg}")
        return None, None

async def fetchPrayerTimes(year : int, month : int, day : int, city : str, method : CalculationMethod, madhab : Madhab, geolocator : Nominatim):
    date = DateComponents(year, month, day)
    params = CalculationParameters(method=method)

    # CRITICAL: Force a high latitude rule to prevent None values during summer/extreme zones
    params.high_latitude_rule = HighLatitudeRule.TWILIGHT_ANGLE

    params.madhab = madhab
    location, local_tz = await fetchLocationAndTzString(city, geolocator)
    coordinates = (float(location["latitude"]), float(location["longitude"]))
    prayer_times = PrayerTimes(coordinates, date, calculation_parameters=params)

    return {"prayer_times": prayer_times, "local_tz": local_tz}