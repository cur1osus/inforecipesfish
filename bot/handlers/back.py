from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.db.models import UserDB, Section
from bot.keyboards.factories import (
    BackFactory,
)
from bot.keyboards.inline import (
    ik_recipe_sections,
    ik_recipes,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.callback_query(BackFactory.filter(F.to == "all_sections"))
async def back_callback_all_sections(
    query: CallbackQuery,
    callback_data: BackFactory,
    user: UserDB,
    session: AsyncSession,
) -> None:
    sections = await session.scalars(select(Section))
    await query.message.edit_reply_markup(
        reply_markup=await ik_recipe_sections(user.is_admin, sections)  # pyright: ignore
    )


@router.callback_query(BackFactory.filter(F.to == "recipes_by_section"))
async def back_callback_recipes_by_section(
    query: CallbackQuery, session: AsyncSession, state: FSMContext, user: UserDB
) -> None:
    data_state = await state.get_data()
    section = await session.get(Section, data_state["section_id"])
    await query.message.edit_text(
        text="Привет!",
        reply_markup=await ik_recipes(
            await section.awaitable_attrs.recipes,
            user.is_admin,
            section.id,
            "all_sections",
        ),
    )
