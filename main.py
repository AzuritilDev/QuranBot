# dependencies/libraries
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time
import asyncio
from os import getenv
from pathlib import Path
from sys import argv
import asyncpg

# load in the .env file
load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
DEV_ENV = getenv("DEV_ENV") # to check if it's dev environment or not
DB_SERVICE_URI = getenv("DB_URL")

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
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        self.launch_time = time.time()

        try:
            self.db_pool = await asyncpg.create_pool(
                dsn=DB_SERVICE_URI,
                min_size=10,
                max_size=19,
                loop=asyncio.get_event_loop(),
                max_inactive_connection_lifetime=300
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
    asyncio.run(main(argv))
except KeyboardInterrupt as e:
    print("[Ctrl + C] Stopped main task.\n", e)