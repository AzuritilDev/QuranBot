import discord
from discord.ext import commands
from utils import quran_fetch, metadata_fetch

verse_range_limit = 10

async def sendQuranVerse(message : discord.Message, chapter : int, verse: int):
    try:
        embed = discord.Embed(title=f"Qur'ân {metadata_fetch.QuranMetadata(chapter)} {chapter}:{verse}", description=quran_fetch.fetch(chapter, verse), color=discord.Color.green())
        embed.set_footer(text="(Sahîh International English Translation)")
        await message.channel.send(embed=embed)
    except Exception as e:
        print("Chat command Qur'ân command error: ", e)

class On_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        if message.author.id == self.bot.user.id:
            return
        
        words = message.content.lower().split(" ")
        if "quran" in words:
            target = words.index("quran")
            if len(words) > target:
                if words[target + 1].count(":") == 1:
                    chapter_and_verse = words[target + 1].split(":")
                    chapter = chapter_and_verse[0]
                    verse = chapter_and_verse[1]
                    if verse.count("-") == 1:
                        verses_range = verse.split("-")
                        verses_start = int(verses_range[0])
                        verses_end = int(verses_range[1])
                        if not (verses_start <= 0 or verses_end < verses_start or verses_end - verses_start > verse_range_limit or int(chapter) <= 0):
                            pass


async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(On_message(bot))