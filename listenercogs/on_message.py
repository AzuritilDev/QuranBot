import discord
from discord.ext import commands
from utils import quran_fetch, metadata_fetch
from cogs.prefix import TTL_EXPIRATION_TIME

verse_range_limit = 10

# safe guard
assert TTL_EXPIRATION_TIME >= 0, "[CRITICAL ERROR] (Prefix Command): Redis does not accept negative expiry. Please change the value to either something equal to zero or something above zero."

async def sendQuranVerse(message : discord.Message, chapter : int, verse : int):
    try:
        embed = discord.Embed(title=f"Qur'ân {metadata_fetch.QuranMetadata(chapter)}, Reference: {chapter}:{verse}", description=quran_fetch.fetch(chapter, verse), color=discord.Color.green())
        embed.set_footer(text="(Sahîh International English Translation)")
        await message.channel.send(embed=embed)
    except Exception as e:
        print("Chat command Qur'ân command error: ", e)

async def sendQuranVerseRanged(message : discord.Message, chapter : int, verses_start : int, verses_end : int, reference : str):
    try:
        embed = discord.Embed(title=f"Qur'ân {metadata_fetch.QuranMetadata(chapter)}, Reference: {chapter}:{verses_start}-{verses_end}", description=quran_fetch.ranged_fetch(reference), color=discord.Color.green())
        embed.set_footer(text="(Sahîh International English Translation)")
        await message.channel.send(embed=embed)
    except Exception as e:
        print("Chat command Qur'ân command error: ", e)

async def sendQuranAny_Forwarder(msg : discord.Message, *params : list[str]):
    reference : str = params[0][0]
    if ":" in reference:
        if "-" in reference.split(":")[1]:
            await sendQuranVerseRanged(
                msg,
                int(reference.split(":")[0]),
                int(reference.split(":")[1].split("-")[0]),
                int(reference.split(":")[1].split("-")[1]),
                reference
            )
        else:
            await sendQuranVerse(
                msg,
                int(reference.split(":")[0]),
                int(reference.split(":")[1]),
            )

# the commands map
cmds = {
    "quran": sendQuranAny_Forwarder
}

async def handle_commands(msg : discord.Message):
    msg_txt = msg.content[1:]
    '''
    stripping away the first character because that's the prefix, 
    handle_commands assumes the first string (the command) doesn't 
    have the prefix
    '''

    cmd, *params = msg_txt.split(" ")
    if cmd in cmds:
        await cmds[cmd](msg, params)

class On_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        if message.author.id == self.bot.user.id:
            return
        
        # prefix based command handling
        if not message.content[0].isalpha() and message.content[0].isascii():
            # is likely a prefix
            cache_key = (
                "prefix:"
                f"{message.guild.id}"
                )

            try:
                # Cache lookup
                cached_prefix = await self.bot.redis.get(cache_key)
            except Exception as e:
                print(f"[REDIS] on_message: An error occured while looking up the prefix for the guild {message.guild.id} ({message.guild.name}): {e}")

            if cached_prefix:
                if cached_prefix == message.content[0]:
                    try:
                        await handle_commands(message)
                    except Exception as e:
                        await message.reply(f"Command handling failed.\nError message:\n```bash\n{e}\n```")
                return
            else:
                # Database lookup
                try:
                    async with self.bot.db_pool.acquire() as cur:
                        row = await cur.fetchrow("""SELECT prefix 
                                           FROM prefixes 
                                           WHERE guild_id = $1""", message.guild.id
                                           )
                        
                        if row == None:
                            # then the guild must be using the default prefix
                            cache_data = self.bot.default_prefix
                            await self.bot.redis.set(cache_key, cache_data, ex=TTL_EXPIRATION_TIME)
                        else:
                            await cur.execute("""
                            INSERT INTO prefixes (guild_id, prefix)
                            VALUES ($1, $2)
                            ON CONFLICT (guild_id)
                            DO UPDATE SET
                                prefix = EXCLUDED.prefix;
                            """, message.guild_id, row[0])
                except Exception as e:
                    print(f"[POSTGRES] on_message: Command prefix handling error: {e}")
                
        # send Qur'ân verse based on whether it's mentioned in the conversation
        words = message.content.lower().split(" ")
        if "quran" in words:
            target = words.index("quran")
            if len(words) > target:
                if words[target + 1].count(":") == 1:
                    chapter_and_verse = words[target + 1].split(":")
                    chapter = chapter_and_verse[0]
                    verse = chapter_and_verse[1]
                    if verse.count("-") == 1:
                        print(1)
                        verses_range = verse.split("-")
                        verses_start = int(verses_range[0])
                        verses_end = int(verses_range[1])
                        if verses_start > 0 and verses_end > verses_start and verses_end - verses_start <= verse_range_limit and int(chapter) > 0 and verses_start != verses_end:
                            await sendQuranVerseRanged(message=message, chapter=int(chapter), verses_start=verses_start, verses_end=verses_end, reference=words[target + 1])
                    else:
                        if int(verse) > 0 and int(chapter) > 0:
                            await sendQuranVerse(message, int(chapter), int(verse))


async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(On_message(bot))