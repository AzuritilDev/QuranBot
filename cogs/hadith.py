import math
import json
import discord
from discord.ext import commands
from discord import app_commands
from utils.hadith_fetch import availableCollections, getHadith
from utils.beautify import Beautify

DEFAULT_TTL = 120

assert DEFAULT_TTL > 0

async def sendHadith(bot : commands.Bot, interaction : discord.Interaction, collection : availableCollections, hadith, hide_response : bool):
    embed = discord.Embed(
                title=f"({Beautify(collection.name)} {hadith['id']})",
                description=hadith['hadith_english'],
                color=bot.signature_color
                                )
    embed.set_author(name=f"{hadith['header']}")
    embed.set_footer(text=f"""Reference No: {hadith['refno']}\nBook Name: {hadith['bookName']}\n{hadith['chapterName']}""", icon_url=bot.user.avatar.url)
    await interaction.followup.send(embed=embed, ephemeral=hide_response)

class Hadith(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hadith", description="Displays a narration.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    @app_commands.choices(collection = [
    app_commands.Choice(
        name=Beautify(item.name),
        value=item.value
    )
    for item in availableCollections])
    async def hadith(self, interaction : discord.Interaction, collection : availableCollections, id : int, hide_response : bool = False):
        await interaction.response.defer(ephemeral=hide_response)
        
        if id <= 0:
            await interaction.followup.send("Please enter a valid hadith ID.", ephemeral=hide_response)

        cache_key = (
            "hadith:"
            f"{collection.value}:"
            f"{id}"
            )
        
        cached = await self.bot.redis.get(cache_key)
        if cached:
            hadith = json.loads(cached)

            await sendHadith(self.bot, interaction, collection,  hadith, hide_response)
        else:
            try:
                hadith, headers, status_code = await getHadith(collection, id)

                await sendHadith(self.bot, interaction, collection, hadith, hide_response)
            except Exception as e:
                if status_code:
                    error_message = f"⚠️`Error Code {status_code}`⚠️\nSomething went wrong, please try again later.\n\nError Message:\n```bash\n{e}\n```"
                else:
                    error_message = f"Something went wrong, please try again later.\n\nError Message:\n```bash\n{e}\n```"
                await interaction.followup.send(error_message, ephemeral=hide_response)
            
            if hadith:
                try:
                    await self.bot.redis.set(
                        cache_key,
                        json.dumps(hadith),
                        ex=DEFAULT_TTL
                    )
                except Exception as e:
                    pass

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Hadith(bot))