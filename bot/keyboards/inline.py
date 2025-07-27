import re

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.models import Recipe, Section
from bot.utils.recipes import SeafoodCategory, recipes

from .factories import (
    AddRecipeFactory,
    AddSectionFactory,
    BackFactory,
    DeleteRecipeFactory,
    DeleteSectionFactory,
    RecipeFactory,
    SectionFactory,
)

recipe_by_category = {
    c: [i for i in recipes.values() if i.category == c] for c in SeafoodCategory
}

ADMIN_NUMBER = -1


async def ik_recipe_sections(is_admin: bool, sections: list[Section]):
    builder = InlineKeyboardBuilder()
    for section in sections:
        builder.button(
            text=section.name, callback_data=SectionFactory(section_id=section.id)
        )
    if is_admin:
        builder.button(
            text="+ Добавить раздел",
            callback_data=AddSectionFactory(section_id=ADMIN_NUMBER),
        )
        builder.button(
            text="- Удалить раздел",
            callback_data=DeleteSectionFactory(section_id=ADMIN_NUMBER),
        )
    builder.adjust(1)
    return builder.as_markup()


async def ik_recipe_sections_to_delete(sections: list[Section]):
    builder = InlineKeyboardBuilder()
    for section in sections:
        builder.button(
            text=section.name, callback_data=DeleteSectionFactory(section_id=section.id)
        )
    builder.button(
        text="Отмена",
        callback_data=BackFactory(to="сancel_section", section_id=ADMIN_NUMBER),
    )
    builder.adjust(1)
    return builder.as_markup()


async def ik_recipes(
    recipes: list[Recipe],
    is_admin: bool,
    section_id: int | str,
    back_to: str = "default",
):
    builder = InlineKeyboardBuilder()
    for recipe in recipes:
        builder.button(
            text=recipe.name, callback_data=RecipeFactory(recipe_id=recipe.id)
        )
    if is_admin:
        builder.button(
            text="+ Добавить рецепт",
            callback_data=AddRecipeFactory(recipe_id=ADMIN_NUMBER),
        )
        builder.button(
            text="- Удалить рецепт",
            callback_data=DeleteRecipeFactory(recipe_id=ADMIN_NUMBER),
        )
    builder.button(
        text="⬅️ Назад",
        callback_data=BackFactory(to=back_to, section_id=int(section_id)),
    )
    builder.adjust(1)
    return builder.as_markup()


async def ik_recipes_to_delete(recipes: list[Recipe]):
    builder = InlineKeyboardBuilder()
    for recipe in recipes:
        builder.button(
            text=recipe.name, callback_data=DeleteRecipeFactory(recipe_id=recipe.id)
        )
    builder.button(
        text="Отмена",
        callback_data=BackFactory(
            to="cancel_recipes", section_id=recipes[0].section_id
        ),
    )
    builder.adjust(1)
    return builder.as_markup()


async def ik_back(back_to: str = "default"):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="* - ❓",
        callback_data="*",
    )
    builder.button(
        text="** - ❓",
        callback_data="**",
    )
    builder.button(
        text="⬅️ Назад",
        callback_data=BackFactory(to=back_to, section_id=ADMIN_NUMBER),
    )
    builder.adjust(1)
    return builder.as_markup()


async def ik_ok(recipe_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ OK",
        callback_data=RecipeFactory(recipe_id=recipe_id),
    )
    builder.adjust(1)
    return builder.as_markup()
