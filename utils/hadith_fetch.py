import requests_async as requests
from enum import Enum

BASE_URL = "https://hadithapi.pages.dev/api"
# Documentation available at: https://hadithapi.pages.dev/docs
# As of writing this, the API above has about 22,000+ narrations
# which should be enough for our case
# Since we are sending HTTP requests, 
# we are going to implement Caching with Redis

class availableCollections(Enum):
    # API slugs regarding collections/authors
    SAHIH_AL_BUKHARI = "bukhari"
    SAHIH_MUSLIM = "muslim"
    SUNAN_ABU_DAWUD = "abudawud"
    SUNAN_IBN_MAJAH = "ibnmajah"
    JAMI_AT_TIRMIDHI = "tirmidhi"

async def getHadith(collection : availableCollections, id : int):
    '''
    Example Request:
        GET /api/bukhari/1
    Example Response:
    {
        "id": 1,
        "header": "Narrated by...",
        "hadith_english": "The hadith text...",
        "book": "Sahih Bukhari",
        "refno": "Bukhari 1",
        "bookName": "Book of Revelation",
        "chapterName": "How the Divine Revelation started"
    }
    '''
    if id <= 0:
        return None

    result = await requests.get(f"{BASE_URL}/{collection.value}/{id}")
    result.raise_for_status() # Raise exception for 4XX/5XX responses
    return result.json(), result.headers, result.status_code
    '''
    NOTE from ALD (@AzuritilDev)
    Regarding headers, the API documentation states:

        Rate Limit Headers

        The API includes the following headers in responses:

        X-RateLimit-Limit: Maximum number of requests allowed per hour
        X-RateLimit-Remaining: Number of requests remaining in the current period
        X-RateLimit-Reset: Time when the rate limit will reset (Unix timestamp)
    
    One of these values can be used to determine the TTL (Time-To-Live) of our Cached values
    '''