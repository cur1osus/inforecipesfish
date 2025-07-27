from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.db.models import Recipe
from bot.keyboards.factories import (
    RecipeFactory,
)
from bot.keyboards.inline import (
    ik_back,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.callback_query(RecipeFactory.filter())
async def recipe_callback(
    query: CallbackQuery,
    callback_data: RecipeFactory,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    recipe = await session.get(Recipe, callback_data.recipe_id)
    await query.message.edit_text(
        text=f"<u>{recipe.name}</u>\n\n{recipe.text}",
        reply_markup=await ik_back(back_to="recipes_by_section"),
    )
    await state.update_data(section_id=recipe.section_id, recipe_id=recipe.id)
