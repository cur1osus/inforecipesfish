from aiogram import Router
from . import start, any_unknow_message

router = Router()

router.include_routers(
    start.router,
    any_unknow_message.router,
)
