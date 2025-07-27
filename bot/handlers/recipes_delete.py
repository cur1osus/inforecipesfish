from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Recipe, Section, UserDB
from bot.keyboards.factories import (
    DeleteRecipeFactory,
)
from bot.keyboards.inline import (
    ADMIN_NUMBER,
    ik_recipes,
    ik_recipes_to_delete,
)

router = Router()


@router.callback_query(DeleteRecipeFactory.filter(F.recipe_id == ADMIN_NUMBER))
async def recipe_delete_callback(
    query: CallbackQuery,
    callback_data: DeleteRecipeFactory,
    session: AsyncSession,
    user: UserDB,
    state: FSMContext,
) -> None:
    data_state = await state.get_data()
    section = await session.get(Section, data_state["section_id"])
    recipes = await section.awaitable_attrs.recipes
    if recipes:
        await query.message.edit_text(
            "Выбери рецепт для удаления",
            reply_markup=await ik_recipes_to_delete(recipes),
        )
    else:
        await query.answer("Рецепты отсутствуют", show_alert=True)


@router.callback_query(DeleteRecipeFactory.filter())
async def apply_recipe_delete_callback(
    query: CallbackQuery,
    callback_data: DeleteRecipeFactory,
    session: AsyncSession,
    user: UserDB,
    state: FSMContext,
) -> None:
    recipe = await session.get(Recipe, callback_data.recipe_id)
    section = await session.get(Section, recipe.section_id)
    recipes = await section.awaitable_attrs.recipes
    recipes.remove(recipe)
    await session.flush()
    await query.message.edit_text(
        "Рецепт удалён",
        reply_markup=await ik_recipes(
            recipes,
            user.is_admin,
            section.id,
            "recipes_by_section",
        ),
    )
    await session.commit()
