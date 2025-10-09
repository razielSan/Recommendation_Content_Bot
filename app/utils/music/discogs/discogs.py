import asyncio
from typing import Dict

from aiogram.fsm.context import FSMContext


def make_update_progress(loop, state: FSMContext):
    """Обновляет прогресс."""

    def update_progress() -> bool:
        data = asyncio.run_coroutine_threadsafe(state.get_data(), loop).result()

        # Обновляем прогресс
        asyncio.run_coroutine_threadsafe(
            state.update_data(counter=data.get("counter", 0) + 1), loop
        ).result()

        return True

    return update_progress


def make_cancel_check(loop, state: FSMContext) -> bool:
    """Возвращает статус состояния отмены для FSM DiscogsFSM

    Returns:
        _type_: Возвращает статус состояния отмены для FSM DiscogsFSM
    """

    def cancel_check():
        data: Dict = asyncio.run_coroutine_threadsafe(state.get_data(), loop).result()
        return data.get("discogs_state", False)

    return cancel_check
