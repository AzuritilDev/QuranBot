import discord
from discord.ext import commands

class On_guild_remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        async with self.bot.db_pool.acquire() as cur:
            await cur.execute("""DELETE FROM dailyquran WHERE guild_id = $1;""", guild.id)


async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(On_guild_remove(bot))