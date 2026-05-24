# dependencies/libraries
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time
import asyncio
from os import getenv
from pathlib import Path
import asyncpg

# load in the .env file
load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
DEV_ENV = getenv("DEV_ENV") # to check if it's dev environment or not
DB_SERVICE_URI = getenv("DB_URL")
CON_MIN_SIZE = getenv("PG_MIN_SIZE") or 10
CON_MAX_SIZE = getenv("PG_MAX_SIZE") or 20
CON_LIFETIME = getenv("PG_LIFETIME") or 300
MAX_QUERIES = getenv("PG_MAX_QUERIES") or 50000

assert DB_SERVICE_URI, "Database service URI is set to None."

# intents
intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.emojis = True
intents.message_content = True

custom_state = """The ˹true˺ believers are only those whose 
hearts tremble at the remembrance of Allah, 
whose faith increases when His revelations are recited to them, 
and who put their trust in their Lord."""

async def initialize_tables(bot):
    async with bot.db_pool.acquire() as cur:
       await cur.execute("""CREATE TABLE IF NOT EXISTS dailyquran (channel_id BIGINT UNIQUE NOT NULL, guild_id BIGINT PRIMARY KEY, webhook_id BIGINT UNIQUE NOT NULL, timezone TEXT);""")

async def cleanup_stale_guilds(bot):
    current_guild_ids = {guild.id for guild in bot.guilds}

    async with bot.db_pool.acquire() as cur:
        rows = await cur.fetch("SELECT guild_id FROM dailyquran")

        for row in rows:
            if row["guild_id"] not in current_guild_ids:
                await cur.execute(
                    "DELETE FROM dailyquran WHERE guild_id = $1",
                    row["guild_id"]
                )

async def cleanup_stale_webhooks(bot):
    rows = await cur.fetch("SELECT guild_id, webhook_id FROM dailyquran")

    async with bot.db_pool.acquire() as cur:
        for row in rows:
            try:
                await bot.fetch_webhook(row["webhook_id"])

            except discord.NotFound:
                await cur.execute(
                    "DELETE FROM dailyquran WHERE guild_id = $1",
                    row["guild_id"]
                )

# bot blueprint
class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        
        self.launch_time = None
        self.db_pool = None
    async def setup_hook(self):
        listenercogs_dir = Path(__file__).parent / "listenercogs"
        listenercogs = [f"listenercogs.{f.stem}" for f in listenercogs_dir.glob("*.py") if not f.name.startswith("_")]

        cogs_dir = Path(__file__).parent / "cogs"
        cogs = [f"cogs.{f.stem}" for f in cogs_dir.glob("*.py") if not f.name.startswith("_")]
        
        all_of_the_cogs = cogs + listenercogs

        print(f"Loading cogs: {all_of_the_cogs}")
        try:
            for ext in all_of_the_cogs:
                await self.load_extension(ext)
        except Exception as e:
            print("Setup hook cogs failed: ", e)

        await initialize_tables(self)
        await cleanup_stale_guilds(self)
        await cleanup_stale_webhooks(self)
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        self.launch_time = time.time()

        try:
            self.db_pool = await asyncpg.create_pool(
                dsn=DB_SERVICE_URI,
                min_size=CON_MIN_SIZE,
                max_size=CON_MAX_SIZE,
                loop=asyncio.get_event_loop(),
                max_inactive_connection_lifetime=CON_LIFETIME,
                max_queries=MAX_QUERIES
            )
            print("Database pool initialized.")
        except Exception as e:
            print("Database pool did not initialize. ", e)

        try:
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name="custom", state=custom_state))
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands.")
        except Exception as e:
            print(e)

# bot object
bot = Client()

# run the bot
async def main():
    await bot.start(BOT_TOKEN)

try:
    asyncio.run(main())
except KeyboardInterrupt as e:
    print("[Ctrl + C] Stopped main task.\n", e)