# dependencies/libraries
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time
import asyncio
from os import getenv
from pathlib import Path
from sys import argv
import sqlite3

# load in the .env file
load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")

# intents
intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.emojis = True
intents.message_content = True

# dev config
path_to_quran_db = "quran.db" # path of the sqlite database file that has or will have the Qur'an verses
'''if this file doesn't exist we will
    create it and import the data
    from utils/quran.sqlite'''

custom_state = """The ˹true˺ believers are only those whose 
hearts tremble at the remembrance of Allah, 
whose faith increases when His revelations are recited to them, 
and who put their trust in their Lord."""

printlog_enabled = False

def printd(text : str):
    if printlog_enabled:
        print(text)


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

        printd(f"Loading cogs: {all_of_the_cogs}")
        try:
            for ext in all_of_the_cogs:
                await self.load_extension(ext)
        except Exception as e:
            printd("Setup hook cogs failed: ", e)
    async def on_ready(self):
        printd(f"Logged in as {self.user}")
        self.launch_time = time.time()
        try:
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name="custom", state=custom_state))
            synced = await self.tree.sync()
            printd(f"Synced {len(synced)} commands.")
        except Exception as e:
            printd(e)

# bot object
bot = Client()

# run the bot
async def main(args):
    # check if quran.db exists, if not, create it
    if not Path(path_to_quran_db).exists():
        con = sqlite3.connect("quran.db")
        printd("Reading & executing quran.sqlite query...")
        with open(Path(__file__).parent / "utils/quran.sqlite", "r") as query:
            query_data = query.read()
            con.cursor().execute(query_data)
            con.close()
            query.close()
            printd("Database file quran.db initialized.")

    # params config during runtime
    if args[0] == "t":
        printlog_enabled = True
    
    await bot.start(BOT_TOKEN)

try:
    asyncio.run(main(argv))
except KeyboardInterrupt as e:
    printd("[Ctrl + C] Stopped main task.\n", e)