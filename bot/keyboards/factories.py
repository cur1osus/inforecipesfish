from aiogram.filters.callback_data import CallbackData


class SectionFactory(CallbackData, prefix="category"):
    section_id: int


class DeleteSectionFactory(CallbackData, prefix="delete_category"):
    section_id: int


class AddSectionFactory(CallbackData, prefix="add_category"):
    section_id: int


class RecipeFactory(CallbackData, prefix="recipe"):
    recipe_id: int


class DeleteRecipeFactory(CallbackData, prefix="delete_recipe"):
    recipe_id: int


class AddRecipeFactory(CallbackData, prefix="add_recipe"):
    recipe_id: int


class BackFactory(CallbackData, prefix="back"):
    to: str
    section_id: int
