import asyncio
from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.Madhab import Madhab
from utils.geography import get_city_coordinates, fetchLocationAndTzString, fetchPrayerTimes, availableTimeFormats, USER_AGENT, GEOPY_CLIENT_TIMEOUT
from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter
from zoneinfo import ZoneInfo

async def test_geography():
    # Test 1: get_city_coordinates() results.
    async with Nominatim(user_agent=USER_AGENT, adapter_factory=AioHTTPAdapter, timeout=GEOPY_CLIENT_TIMEOUT) as geolocator:
        city_coordinates_raw = {'latitude': 21.420847, 'longitude': 39.826869}
        city_coordinates_result = await get_city_coordinates(theCity="Makkah", bot_geolocator=geolocator)
        print(city_coordinates_raw, city_coordinates_result)
        assert city_coordinates_raw == city_coordinates_result, "Raw coordinates data does not match the fetched result. [get_city_coordinates()]"

    # Test 2: fetchLocationAndTzString() results.
    async with Nominatim(user_agent=USER_AGENT, adapter_factory=AioHTTPAdapter, timeout=GEOPY_CLIENT_TIMEOUT) as geolocator:
        location_raw, tz_string_raw = {'latitude': 21.420847, 'longitude': 39.826869}, "Asia/Riyadh"
        location, tz_string = await fetchLocationAndTzString(city="Makkah", geolocator=geolocator)
        print(location, tz_string)
        assert location_raw == location, "Locations don't match. [fetchLocationAndTzString()]"
        assert tz_string_raw == tz_string, "Tz Strings don't match. [fetchLocationAndTzString()]"
    
    # Test 3: fetchPrayerTimes() results.
    async with Nominatim(user_agent=USER_AGENT, adapter_factory=AioHTTPAdapter, timeout=GEOPY_CLIENT_TIMEOUT) as geolocator:
        prayer_times = await fetchPrayerTimes(2026, 6, 14, "Makkah", CalculationMethod.UMM_AL_QURA, Madhab.HANAFI, geolocator)
        print(prayer_times)

        actual_prayer_times = prayer_times["prayer_times"]
        tz = ZoneInfo(prayer_times["local_tz"])
        format_1 = availableTimeFormats.TWENTY_FOUR_HOUR_MILITARY_TIME.value
        format_2 = availableTimeFormats.TWELVE_HOUR_TIME.value

        assert actual_prayer_times.fajr.astimezone(tz).strftime(format_1) == "04:10"
        assert actual_prayer_times.sunrise.astimezone(tz).strftime(format_1) == "05:38"
        assert actual_prayer_times.dhuhr.astimezone(tz).strftime(format_1) == "12:21"
        assert actual_prayer_times.asr.astimezone(tz).strftime(format_1) == "16:59"
        assert actual_prayer_times.maghrib.astimezone(tz).strftime(format_1) == "19:04"
        assert actual_prayer_times.isha.astimezone(tz).strftime(format_1) == "20:34"

        assert actual_prayer_times.fajr.astimezone(tz).strftime(format_2) == "04:10 AM"
        assert actual_prayer_times.sunrise.astimezone(tz).strftime(format_2) == "05:38 AM"
        assert actual_prayer_times.dhuhr.astimezone(tz).strftime(format_2) == "12:21 PM"
        assert actual_prayer_times.asr.astimezone(tz).strftime(format_2) == "04:59 PM"
        assert actual_prayer_times.maghrib.astimezone(tz).strftime(format_2) == "07:04 PM"
        assert actual_prayer_times.isha.astimezone(tz).strftime(format_2) == "08:34 PM"