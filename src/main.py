from config import config
from ldap_service import LDAPService
import interactions
from interactions.ext import prefixed_commands
from loguru import logger

DISCORD_MESSAGE_LENGTH = 2000
DISCORD_CHOICE_LENGTH = 25
MESSAGE_DELETE_DELAY = 600

intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
bot = interactions.Client(intents=intents, sync_interactions=True, asyncio_debug=True, logger=logger)
prefixed_commands.setup(bot)
ldap_service = LDAPService()

@interactions.listen()
async def on_ready():
    logger.info(f"This bot is owned by {bot.owner}")

@interactions.slash_command(name="聯絡人", description='找出ACTG的聯絡人資訊!')
@interactions.slash_option(
    name="search_string",
    description="搜尋字串",
    required=True,
    autocomplete=True,
    opt_type=interactions.OptionType.STRING,
)
async def search_contacts(ctx: interactions.SlashContext, search_string: str):
    await ctx.defer()
    result_lists = ldap_service.search(search_string, DISCORD_MESSAGE_LENGTH)
    for r in result_lists:
        message = await ctx.send(r)
        await message.delete(MESSAGE_DELETE_DELAY)

@search_contacts.autocomplete("search_string")
async def autocomplete(ctx: interactions.AutocompleteContext):
    # make sure this is done within three seconds
    await ctx.send(
        choices=ldap_service.autocomplete_search(ctx.input_text)[:DISCORD_CHOICE_LENGTH]
    )
    
if __name__ == "__main__":
    bot.start(config.discord_token)