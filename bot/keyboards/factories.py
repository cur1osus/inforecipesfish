from aiogram.filters.callback_data import CallbackData
from bot.utils.recipes import SeafoodCategory
from typing import Any


class RecipeFactory(CallbackData, prefix="rf"):
    recipe_id: int


class RecipeCategoryFactory(CallbackData, prefix="rcf"):
    category: SeafoodCategory


class BackFactory(CallbackData, prefix="bf"):
    to: str


class CallbackStorageFactory(CallbackData, prefix="csf"):
    callback_data: str
    value: Any
