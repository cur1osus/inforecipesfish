from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.db.models import UserDB, Section
from bot.keyboards.factories import (
    AddSectionFactory,
)
from bot.keyboards.inline import (
    ik_recipe_sections,
    ADMIN_NUMBER,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states import UserState

router = Router()


@router.callback_query(AddSectionFactory.filter(F.section_id == ADMIN_NUMBER))
async def recipe_section_admin_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await query.message.edit_text(text="Введи название раздела:")
    await state.set_state(UserState.recipe_section_enter_name)


@router.message(UserState.recipe_section_enter_name)
async def get_recipe_section_name(
    message: Message, state: FSMContext, session: AsyncSession, user: UserDB
) -> None:
    section = Section(name=message.text)
    session.add(section)
    await session.flush()
    sections = await session.scalars(select(Section))
    await message.answer(
        text="Раздел создан",
        reply_markup=await ik_recipe_sections(user.is_admin, sections),  # pyright: ignore
    )
    await session.commit()
    await state.clear()
    await state.update_data(section_id=section.id)
