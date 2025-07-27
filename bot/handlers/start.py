from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from bot.keyboards.factories import (
    BackFactory,
    RecipeCategoryFactory,
    RecipeFactory,
    CallbackStorageFactory,
)
from bot.keyboards.inline import ik_back, ik_recipe_categories, ik_recipes, ik_ok
from bot.utils.recipes import (
    SeafoodCategory,
    recipes,
    additional_information_star,
    additional_information_stars,
)

router = Router()


@router.message(CommandStart())
async def command_start(
    message: Message,
) -> None:
    await message.answer(text="Привет!", reply_markup=await ik_recipe_categories())


@router.callback_query(RecipeCategoryFactory.filter())
async def recipe_category_callback(
    query: CallbackQuery,
    callback_data: RecipeCategoryFactory,
) -> None:
    await query.message.edit_reply_markup(
        reply_markup=await ik_recipes(callback_data.category)
    )


@router.callback_query(RecipeFactory.filter())
async def recipe_callback(
    query: CallbackQuery,
    callback_data: RecipeFactory,
) -> None:
    recipe = recipes.get(callback_data.recipe_id)
    await query.message.edit_text(
        text=f"<u>{recipe.name}</u>\n\n<b>*Ингредиенты:</b>\n{',\n'.join(recipe.ingredients)}\n\n<b>**Рецепт:</b>\n{' '.join(recipe.instructions)}",
        reply_markup=await ik_back(back_to=recipe.category.value, recipe_id=recipe.id),
    )


@router.callback_query(BackFactory.filter(F.to == "categories"))
async def back_callback(
    query: CallbackQuery,
    callback_data: BackFactory,
) -> None:
    await query.message.edit_reply_markup(reply_markup=await ik_recipe_categories())


@router.callback_query(BackFactory.filter(F.to.in_(SeafoodCategory)))
async def back_callback_seafood(
    query: CallbackQuery,
    callback_data: BackFactory,
) -> None:
    category = (
        SeafoodCategory(callback_data.to)
        if isinstance(callback_data.to, str)
        else SeafoodCategory.WHITE_FISH
    )
    await query.message.edit_text(
        text="Привет!", reply_markup=await ik_recipes(category)
    )


@router.callback_query(CallbackStorageFactory.filter(F.callback_data == "*"))
async def info_star(
    query: CallbackQuery,
    callback_data: CallbackStorageFactory,
) -> None:
    await query.message.edit_text(
        text=additional_information_star,
        reply_markup=await ik_ok(recipe_id=callback_data.value),
    )


@router.callback_query(CallbackStorageFactory.filter(F.callback_data == "**"))
async def info_stars(
    query: CallbackQuery,
    callback_data: CallbackStorageFactory,
) -> None:
    await query.message.edit_text(
        text=additional_information_stars,
        reply_markup=await ik_ok(recipe_id=callback_data.value),
    )
