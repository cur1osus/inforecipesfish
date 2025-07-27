from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message()
async def any_unknow_message(message: Message) -> None:
    await message.answer("Не понял вас")
