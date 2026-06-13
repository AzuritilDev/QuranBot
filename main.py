# dependencies/libraries
import discord
from discord.ext import commands, tasks
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
CON_MIN_SIZE = int(getenv("PG_MIN_SIZE", 10))
CON_MAX_SIZE = int(getenv("PG_MAX_SIZE", 20))
CON_LIFETIME = float(getenv("PG_LIFETIME", 300))
MAX_QUERIES = int(getenv("PG_MAX_QUERIES", 50000))

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
    print("Initializing database tables...")
    async with bot.db_pool.acquire() as cur:
       await cur.execute("""CREATE TABLE IF NOT EXISTS dailyquran (channel_id BIGINT UNIQUE NOT NULL, guild_id BIGINT PRIMARY KEY, webhook_id BIGINT UNIQUE NOT NULL, timezone TEXT, last_sent_date DATE);""")

async def cleanup_stale_guilds(bot):
    print("Cleaning up stale guilds...")
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
    print("Cleaning up stale webhooks...")
    
    # Open the connection block FIRST
    async with bot.db_pool.acquire() as conn:
        # NOW execute the fetch using 'conn' inside the block
        rows = await conn.fetch("SELECT guild_id, webhook_id FROM dailyquran")
        
        for row in rows:
            try:
                await bot.fetch_webhook(row["webhook_id"])

            except discord.NotFound:
                await conn.execute(
                    "DELETE FROM dailyquran WHERE guild_id = $1",
                    row["guild_id"]
                )

# bot blueprint
class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        
        self.launch_time = None
        self.db_pool = None
        self.signature_color = discord.Color.green()
    async def setup_hook(self):
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

        loopcogs_dir = Path(__file__).parent / "loopcogs"
        loopcogs = [f"loopcogs.{f.stem}" for f in loopcogs_dir.glob("*.py") if not f.name.startswith("_")]

        listenercogs_dir = Path(__file__).parent / "listenercogs"
        listenercogs = [f"listenercogs.{f.stem}" for f in listenercogs_dir.glob("*.py") if not f.name.startswith("_")]

        cogs_dir = Path(__file__).parent / "cogs"
        cogs = [f"cogs.{f.stem}" for f in cogs_dir.glob("*.py") if not f.name.startswith("_")]
        
        all_of_the_cogs = cogs + listenercogs + loopcogs

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