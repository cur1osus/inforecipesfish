from aiogram import Router

from . import (
    additional_info,
    any_unknow_message,
    back,
    cancel,
    recipes,
    recipes_add,
    recipes_delete,
    section,
    section_add,
    section_delete,
    start,
)

router = Router()

router.include_routers(
    start.router,
    recipes.router,
    recipes_add.router,
    recipes_delete.router,
    section.router,
    section_add.router,
    section_delete.router,
    cancel.router,
    back.router,
    additional_info.router,
    any_unknow_message.router,
)
