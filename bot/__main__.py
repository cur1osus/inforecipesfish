from __future__ import annotations

import asyncio
import logging
from asyncio import CancelledError

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import PRODUCTION
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.types import BotCommand

from bot import handlers
from bot.settings import se, Settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def startup(dispatcher: Dispatcher, bot: Bot, se: Settings) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.send_message(chat_id=se.developer_id, text="Bot started")


async def shutdown(dispatcher: Dispatcher) -> None:
    logger.info("Bot stopped")


async def set_default_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="start"),
        ]
    )


async def main() -> None:
    api = PRODUCTION

    bot = Bot(
        token=se.bot_token,
        session=AiohttpSession(api=api),
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher(
        events_isolation=SimpleEventIsolation(),
        se=se,
        developer_id=se.developer_id,
    )

    dp.include_routers(handlers.router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await set_default_commands(bot)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        uvloop = __import__("uvloop")
        loop_factory = uvloop.new_event_loop

    except ModuleNotFoundError:
        loop_factory = asyncio.new_event_loop
        logger.info("uvloop not found, using default event loop")

    try:
        with asyncio.Runner(loop_factory=loop_factory) as runner:
            runner.run(main())

    except (CancelledError, KeyboardInterrupt):
        __import__("sys").exit(0)
