# Privacy Policy for QuranBot
Last updated: 2 July 2026 (GMT+3)

**1. Data We Process and Store**
* **Persistent Database Storage:** We operate a secure relational database and a secure in-memory database to store functional system configurations. This includes Discord Server IDs, Channel IDs, and bot settings (e.g., active alert toggles). No personal data or user histories are stored here.
* **Temporary Cache of Location Data (No Permanent Storage):** When you request prayer times for a specific city or geographic coordinate, this information is processed to calculate the requested prayer times. To improve performance, the bot temporarily caches prayer time results in a password-protected Redis instance. The cache key may include the requested city name, and cached entries automatically expire after a limited period. This data is not stored permanently, is not publicly accessible, and is used solely to improve the efficiency of repeated prayer time requests.

**2. Data Retention and Deletion**
* **Configuration Retention:** Discord channel configuration data is saved in our relational database until the bot is removed from the server, or until a server administrator resets the configuration settings.
* **Ephemeral Processing:** All location inputs are strictly volatile, session-based, and short-lived.

**3. Data Sharing**
* We do not sell, trade, or share any data with third parties. All astronomical calculations via the `adhanpy` library happen completely locally within our secure hosting environment. No data is transmitted externally.

**4. Support and Contact**
* If you have any questions about this Privacy Policy, encounter bugs, or need assistance, you can reach out directly via the following channels:
    * **Email:** azuriteluadev@proton.me
    * **GitHub Issues:** Open an issue on our official GitHub repository (https://github.com/AzuritilDev/QuranBot).
