import asyncio
from src.config import config
from src.db import RedisClient
from src.contact_service import ContactService
from src.ldap_service import LDAPService
from src.utils import caculate_editdistance
import interactions
from interactions.ext import prefixed_commands
from loguru import logger
import re

DISCORD_MESSAGE_LENGTH = 2000
DISCORD_CHOICE_LENGTH = 25
MESSAGE_DELETE_DELAY = 600

intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
bot = interactions.Client(
    intents=intents, sync_interactions=True, asyncio_debug=False, logger=logger
)
prefixed_commands.setup(bot)
contact_service = ContactService()
ldap_service = LDAPService()
redis_client = RedisClient()


@interactions.listen()
async def on_ready():
    logger.info(f"This bot is owned by {bot.owner}")


@interactions.slash_command(name="聯絡人", description="找出ACTG的聯絡人資訊!")
@interactions.slash_option(
    name="search_string",
    description="搜尋字串",
    required=True,
    autocomplete=True,
    opt_type=interactions.OptionType.STRING,
)
async def search_contacts(ctx: interactions.SlashContext, search_string: str):
    await ctx.defer()
    ldap_coro = ldap_service.search(search_string, DISCORD_MESSAGE_LENGTH)
    contact_coro = contact_service.search(search_string, DISCORD_MESSAGE_LENGTH)

    for result in await ldap_coro:
        result = "**----------- LDAP ----------**\n" + result
        message = await ctx.send(result)
        await message.delete(MESSAGE_DELETE_DELAY)

    for result in await contact_coro:
        result = "**----------- Excel ----------**\n" + result
        message = await ctx.send(result)
        await message.delete(MESSAGE_DELETE_DELAY)


@search_contacts.autocomplete("search_string")
async def autocomplete(ctx: interactions.AutocompleteContext):
    if ctx.input_text == "":
        await ctx.send(choices=[])
    else:
        # make sure this is done within three seconds
        await ctx.send(
            choices=ldap_service.autocomplete_search(ctx.input_text)[
                :DISCORD_CHOICE_LENGTH
            ]
        )


if __name__ == "__main__":
    bot.start(config.discord_token)
