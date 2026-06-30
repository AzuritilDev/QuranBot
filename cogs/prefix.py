import discord
from discord.ext import commands
from discord import app_commands

TTL_EXPIRATION_TIME = 24 * 60 * 60 # 1 day

'''
Here we save the prefix to not only the disk but also the in-memory database
Because if we query the relational database everytime someone sends a message
it will be pretty slow, which is why we cache the prefix
'''
class Prefix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="prefix", description="Sets the preferred prefix for the bot based on the guild (Discord server).")
    async def prefixcmd(self, interaction: discord.Interaction, prefix : str, hide_response : bool = False):
        '''The prefix input must meet the following criteria:
            - Must not be longer than 1 character.
            - Must be an ASCII CHARACTER.
            If the entered prefix is the bot's default prefix, 
            it will not be saved to the database 
            and existing records of it in the database will be removed. 
        '''
        if len(prefix) > 1:
            interaction.response.send_message("The prefix can only be a single character like ',' or '!'.\nNot full words, phrases or sentences.", ephemeral=hide_response)
        elif not prefix.isascii():
            interaction.response.send_message(f"The prefix must be an ASCII character.\n\nYou entered: {prefix}", ephemeral=hide_response)
        elif prefix == " " or prefix == self.bot.default_prefix:
            await interaction.response.defer(ephemeral=hide_response)
            try:
                async with self.bot.db_pool.acquire() as cur:
                    await cur.execute("""
                                DELETE FROM prefixes
                                WHERE guild_id = $1
                                """, interaction.guild_id)
            except Exception as e:
                await interaction.followup.send(f"[POSTGRES] Something went wrong while removing the existing prefix from the database.\n\nError message: {e}", ephemeral=hide_response)
            await interaction.followup.send(f"The prefix for the guild '{interaction.guild.name}' `(id:{interaction.guild_id})` has been set to `{prefix}` (The default prefix).\nBecause you either entered an empty prefix or the default prefix of the bot which is `{self.bot.default_prefix}`.", ephemeral=hide_response)

        await interaction.response.defer(ephemeral=hide_response)

        try:
            async with self.bot.db_pool.acquire() as cur:
                await cur.execute("""
                            INSERT INTO prefixes (guild_id, prefix)
                            VALUES ($1, $2)
                            ON CONFLICT (guild_id)
                            DO UPDATE SET
                                prefix = EXCLUDED.prefix;
                            """, interaction.guild_id, prefix)
        except Exception as e:
            await interaction.followup.send(f"[POSTGRES] Something went wrong while saving the prefix into the database.\n\nError message: {e}", ephemeral=hide_response)

        cache_key = (
            f"prefix:"
            f"{interaction.guild_id}"
        )

        cache_data = prefix
        
        try:
            await self.bot.redis.set(
                cache_key,
                cache_data,
                ex=TTL_EXPIRATION_TIME
            )
        except Exception as e:
            await interaction.followup.send("[REDIS] Something went wrong while saving the prefix into the in-memory database.\n\nError message: {e}", ephemeral=hide_response)

        await interaction.followup.send(f"The prefix for the guild '{interaction.guild.name}' `(id:{interaction.guild_id})` has been set to `{prefix}`.", ephemeral=hide_response)

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(Prefix(bot))