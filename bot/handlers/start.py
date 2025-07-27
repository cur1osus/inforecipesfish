from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.db.models import UserDB, Section
from bot.keyboards.inline import (
    ik_recipe_sections,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_cmd_with_deep_link(
    message: Message,
    command: CommandObject,
    sessionmaker,
    state: FSMContext,
    user: UserDB,
) -> None:
    args = command.args.split() if command.args else []
    deep_link = args[0]
    if deep_link == "true":
        async with sessionmaker() as session:
            _user = await session.get(UserDB, user.id)
            _user.is_admin = True
            sections = await session.scalars(select(Section))
            await message.answer(
                text="Привет! Теперь ты администратор",
                reply_markup=await ik_recipe_sections(_user.is_admin, sections),  # pyright: ignore
            )
            await session.commit()


@router.message(CommandStart())
async def command_start(message: Message, user: UserDB, session: AsyncSession) -> None:
    sections = await session.scalars(select(Section))
    await message.answer(
        text="Привет!",
        reply_markup=await ik_recipe_sections(user.is_admin, sections),  # pyright: ignore
    )
