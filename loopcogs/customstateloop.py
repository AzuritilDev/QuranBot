import discord
import random
from discord.ext import commands, tasks
from utils.custom_states import quotes

class StateLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Start the loop right when the Cog loads
        self.custom_state_task.start()

    @tasks.loop(hours=1)
    async def custom_state_task(self):
        selected_quote = random.choice(quotes)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name="custom", state=selected_quote))
    
    @custom_state_task.before_loop
    async def before_custom_state_task(self):
        # Wait for Discord to be fully ready
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.custom_state_task.cancel()

async def setup(bot):
    await bot.add_cog(StateLoop(bot))