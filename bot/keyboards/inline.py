import re
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.utils.recipes import recipes, SeafoodCategory
from .factories import (
    RecipeFactory,
    RecipeCategoryFactory,
    BackFactory,
    CallbackStorageFactory,
)

recipe_by_category = {
    c: [i for i in recipes.values() if i.category == c] for c in SeafoodCategory
}


async def ik_recipe_categories():
    builder = InlineKeyboardBuilder()
    for category in SeafoodCategory:
        builder.button(
            text=category.value, callback_data=RecipeCategoryFactory(category=category)
        )
    builder.adjust(1)
    return builder.as_markup()


async def ik_recipes(category: SeafoodCategory):
    builder = InlineKeyboardBuilder()
    for recipe in recipe_by_category[category]:
        builder.button(
            text=recipe.name, callback_data=RecipeFactory(recipe_id=recipe.id)
        )
    builder.button(text="⬅️ Назад", callback_data=BackFactory(to="categories"))
    builder.adjust(1)
    return builder.as_markup()


async def ik_back(recipe_id: int | str, back_to: str = "default"):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="* - ❓",
        callback_data=CallbackStorageFactory(callback_data="*", value=recipe_id),
    )
    builder.button(
        text="** - ❓",
        callback_data=CallbackStorageFactory(callback_data="**", value=recipe_id),
    )
    builder.button(
        text="⬅️ Назад",
        callback_data=BackFactory(to=back_to),
    )
    builder.adjust(1)
    return builder.as_markup()


async def ik_ok(recipe_id: int | str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ OK",
        callback_data=RecipeFactory(recipe_id=int(recipe_id)),
    )
    builder.adjust(1)
    return builder.as_markup()
