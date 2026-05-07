import discord
from discord.ext import commands

class On_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
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
                        pass

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(On_message(bot))