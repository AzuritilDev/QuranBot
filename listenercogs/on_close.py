from discord.ext import commands

class On_close(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def close(self):
        print("Shutting down bot...")
        if self.redis:
            await self.redis.close()
            print("Redis Cluster connection closed.")
        if self.db_pool:
            await self.db_pool.close()
            print("PostgreSQL Database connection pool closed.")
        await super().close()

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(On_close(bot))