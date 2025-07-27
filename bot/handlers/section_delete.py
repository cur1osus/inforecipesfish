from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.db.models import UserDB, Section
from bot.keyboards.factories import (
    DeleteSectionFactory,
)
from bot.keyboards.inline import (
    ik_recipe_sections,
    ADMIN_NUMBER,
    ik_recipe_sections_to_delete,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.callback_query(DeleteSectionFactory.filter(F.section_id == ADMIN_NUMBER))
async def recipe_section_delete_callback(
    query: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    sections = await session.scalars(select(Section))
    if sections:
        await query.message.edit_text(
            text="Выбери раздел для удаления",
            reply_markup=await ik_recipe_sections_to_delete(sections),  # pyright: ignore
        )
    else:
        await query.answer(text="Разделы отсутствуют", show_alert=True)


@router.callback_query(DeleteSectionFactory.filter())
async def apply_section_delete_callback(
    query: CallbackQuery,
    state: FSMContext,
    callback_data: DeleteSectionFactory,
    session: AsyncSession,
    user: UserDB,
) -> None:
    section = await session.get(Section, callback_data.section_id)
    await session.delete(section)
    await session.flush()
    sections = await session.scalars(select(Section))
    await session.commit()
    await query.message.edit_text(
        text="Раздел успешно удален",
        reply_markup=await ik_recipe_sections(user.is_admin, sections),  # pyright: ignore
    )
