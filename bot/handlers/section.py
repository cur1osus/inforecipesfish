from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.db.models import UserDB, Section
from bot.keyboards.factories import (
    SectionFactory,
)
from bot.keyboards.inline import (
    ik_recipes,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.callback_query(SectionFactory.filter())
async def recipe_section_callback(
    query: CallbackQuery,
    callback_data: SectionFactory,
    session: AsyncSession,
    user: UserDB,
    state: FSMContext,
) -> None:
    section = await session.get(Section, callback_data.section_id)
    recipes = await section.awaitable_attrs.recipes
    await query.message.edit_reply_markup(
        reply_markup=await ik_recipes(
            recipes, user.is_admin, section.id, "all_sections"
        )
    )
    if user.is_admin:
        await state.update_data(section_id=section.id)
