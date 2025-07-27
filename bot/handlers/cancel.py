from aiogram import F, Router
from aiogram.types import CallbackQuery

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


@router.callback_query(BackFactory.filter(F.to == "сancel_section"))
async def back_callback_cancel_section(
    query: CallbackQuery,
    callback_data: BackFactory,
    user: UserDB,
    session: AsyncSession,
) -> None:
    sections = await session.scalars(select(Section))
    await query.message.edit_reply_markup(
        reply_markup=await ik_recipe_sections(user.is_admin, sections)  # pyright: ignore
    )


@router.callback_query(BackFactory.filter(F.to == "cancel_recipes"))
async def back_callback_cancel_recipes(
    query: CallbackQuery,
    callback_data: BackFactory,
    user: UserDB,
    session: AsyncSession,
) -> None:
    section = await session.get(Section, callback_data.section_id)
    await query.message.edit_reply_markup(
        reply_markup=await ik_recipes(
            await section.awaitable_attrs.recipes,
            user.is_admin,
            section.id,
            "all_sections",
        )
    )  # pyright: ignore
