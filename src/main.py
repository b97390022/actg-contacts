import interactions
from interactions.ext import prefixed_commands
from loguru import logger

from src.config import config
from src.controller.contact_controller import ContactController, SeatingChartController
from src.controller.ldap_controller import LDAPController

DISCORD_MESSAGE_LENGTH = 2000
DISCORD_CHOICE_LENGTH = 25
MESSAGE_DELETE_DELAY = 600
DELIMITER_COUNT = 20

intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
bot = interactions.Client(
    intents=intents, sync_interactions=True, asyncio_debug=False, logger=logger
)
prefixed_commands.setup(bot)
contact_controller = ContactController()
seating_chart_controller = SeatingChartController()
ldap_controller = LDAPController()

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
    ldap_coro = ldap_controller.search(search_string, DISCORD_MESSAGE_LENGTH)
    contact_coro = contact_controller.search(search_string, DISCORD_MESSAGE_LENGTH)

    for result in await ldap_coro:
        result = f"**{DELIMITER_COUNT*'-'} LDAP {DELIMITER_COUNT*'-'}**\n" + result
        await ctx.send(result)
        # await message.delete(MESSAGE_DELETE_DELAY)

    for result in await contact_coro:
        result = f"**{DELIMITER_COUNT*'-'} Excel {DELIMITER_COUNT*'-'}**\n" + result
        await ctx.send(result)
        # await message.delete(MESSAGE_DELETE_DELAY)


@interactions.slash_command(name="聯絡人座位圖", description="找出ACTG的聯絡人座位!")
@interactions.slash_option(
    name="search_string",
    description="搜尋字串",
    required=True,
    autocomplete=True,
    opt_type=interactions.OptionType.STRING,
)
async def search_seating_chart(ctx: interactions.SlashContext, search_string: str):
    await ctx.defer()
    seating_coro = seating_chart_controller.search(search_string)

    images_path = await seating_coro
    if not images_path:
        text = f"**{DELIMITER_COUNT*'-'} 座位圖 {DELIMITER_COUNT*'-'}**\n"
        text+= "找不到結果！"
        await ctx.send(text)

    else:
        for image_path in images_path:
            text = f"**{DELIMITER_COUNT*'-'} 座位圖 {DELIMITER_COUNT*'-'}**\n"
            await ctx.send(text, file=image_path)


@search_contacts.autocomplete("search_string")
@search_seating_chart.autocomplete("search_string")
async def autocomplete(ctx: interactions.AutocompleteContext):
    if ctx.input_text == "":
        await ctx.send(choices=[])
    else:
        # make sure this is done within three seconds
        await ctx.send(
            choices=ldap_controller.autocomplete_search(ctx.input_text)[
                :DISCORD_CHOICE_LENGTH
            ]
        )


if __name__ == "__main__":
    bot.start(config.discord_token)
