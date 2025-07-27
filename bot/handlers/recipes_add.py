from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.db.models import UserDB, Section, Recipe
from bot.keyboards.factories import (
    AddRecipeFactory,
)
from bot.keyboards.inline import (
    ik_recipes,
    ADMIN_NUMBER,
)
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states import UserState

router = Router()


@router.callback_query(AddRecipeFactory.filter(F.recipe_id == ADMIN_NUMBER))
async def recipe_admin_callback(
    query: CallbackQuery,
    callback_data: AddRecipeFactory,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    await query.message.edit_text("Введи название рецепта")
    await state.set_state(UserState.recipe_enter_name)


@router.message(UserState.recipe_enter_name)
async def recipe_enter_name(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    await state.update_data(name_recipe=message.text)
    await message.answer("Введи текст рецепта")
    await state.set_state(UserState.recipe_enter_text)


@router.message(UserState.recipe_enter_text)
async def recipe_enter_text(
    message: Message, state: FSMContext, session: AsyncSession, user: UserDB
) -> None:
    data_state = await state.get_data()
    recipe = Recipe(name=data_state["name_recipe"], text=message.text)
    section = await session.get(Section, data_state["section_id"])
    recipes = await section.awaitable_attrs.recipes
    recipes.append(recipe)
    await session.commit()
    await state.clear()
    await state.update_data(section_id=section.id)
    await message.answer(
        "Рецепт успешно добавлен!",
        reply_markup=await ik_recipes(
            recipes, user.is_admin, section.id, "all_sections"
        ),
    )
