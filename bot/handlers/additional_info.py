from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline import (
    ik_ok,
)
from bot.utils.recipes import additional_information_stars, additional_information_star

router = Router()


@router.callback_query(F.data == "*")
async def info_star(query: CallbackQuery, state: FSMContext) -> None:
    data_state = await state.get_data()
    await query.message.edit_text(
        text=additional_information_star,
        reply_markup=await ik_ok(recipe_id=data_state["recipe_id"]),
    )


@router.callback_query(F.data == "**")
async def info_stars(query: CallbackQuery, state: FSMContext) -> None:
    data_state = await state.get_data()
    await query.message.edit_text(
        text=additional_information_stars,
        reply_markup=await ik_ok(recipe_id=data_state["recipe_id"]),
    )
