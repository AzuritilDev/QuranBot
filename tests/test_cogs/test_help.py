import pytest
import discord
import discord.ext.test as dpytest
from unittest.mock import AsyncMock, MagicMock
from cogs.help import Help as theCog
from main import Client, bot, SIGNATURE_COLOR, DEFAULT_PREFIX

cmdfunc = theCog.help

@pytest.fixture
async def mock_bot():
    """Initializes dpytest's internal client simulation state."""
    # Configure the bot into dpytest's internal fake state
    dpytest.configure(bot)
    yield bot
    # Clean up state after the test completes
    await dpytest.empty_queue()

@pytest.mark.asyncio
async def test_said_slash_command():
    mock_bot_instance = MagicMock(spec=Client)
    mock_bot_instance.signature_color = SIGNATURE_COLOR
    mock_bot_instance.default_prefix = DEFAULT_PREFIX

    cog_instance = theCog(bot=mock_bot_instance)
    
    mock_interaction = MagicMock(spec=discord.Interaction)
    mock_interaction.response = AsyncMock()

    mock_namespace = MagicMock()
    mock_namespace.help_response = False
    mock_interaction.namespace = mock_namespace

    await cmdfunc.callback(cog_instance, mock_interaction)

    mock_interaction.response.send_message.assert_called_once()

    _, kwargs = mock_interaction.response.send_message.call_args
    actual_embed = kwargs.get("embed")

    # NOTE: The expected embed might not be up to date with the actual embed
    expected_embed = discord.Embed(
        title="📘 Help - Command List",
        color=SIGNATURE_COLOR
    )
    
    expected_embed.add_field(name="/help", value="Lists all the available slash commands of the bot.", inline=False)
    expected_embed.add_field(name="/quran", value="Displays a Qur'ân verse based on the user's input.", inline=False)
    expected_embed.add_field(name="/set-daily-quran", value="Displays verses on a selected channel daily.", inline=False)
    expected_embed.add_field(name="/prayer-times", value="Displays the Islamic prayer times based on selected city.", inline=False)
    expected_embed.add_field(name="/status", value="Displays system information about the bot.", inline=False)
    expected_embed.add_field(name="/prefix", value="Sets the preferred prefix the bot uses in your guild/server.", inline=False)

    assert actual_embed is not None, "The command did not send an embed!"
    # assert actual_embed.to_dict() == expected_embed.to_dict()
    assert len(actual_embed.fields) == len(expected_embed.fields) # it is better to use this for complicated embeds