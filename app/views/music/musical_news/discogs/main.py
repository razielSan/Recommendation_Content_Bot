from typing import List, Dict
from datetime import datetime
import asyncio
from asyncio import Future

from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config.music import discogs_setting
from keyboards.music.inline import get_discogs_menu_button
from keyboards.reply import get_main_menu_button
from keyboards.reply import get_cancel_button
from keyboards.inline import get_button_for_forward_or_back
from functions.music import get_list_albums_for_discogs, get_descripions_for_albums
from extensions import bot


router: Router = Router(name=__name__)


@router.callback_query(StateFilter(None), F.data == discogs_setting.CALLBACK_DISCOGS)
async def main(call: CallbackQuery):
    """Возвращает инлайн клавиатуру с выборами вариантов жанров для discogs.com."""
    await call.message.answer(
        text="Доступные варианты",
        reply_markup=get_discogs_menu_button(),
    )


class DiscogsFSM(StatesGroup):
    """FSM для работы с сайтом discogs.com."""
    albums_list: State = State()
    discogs_state: State = State()


@router.message(DiscogsFSM.discogs_state, F.text == "Отмена")
@router.message(DiscogsFSM.albums_list, F.text == "Отмена")
async def cancel_discogs_handler(message: Message, state=FSMContext):
    """Работа с FSM DiscogsFSM.Отменяет все действия."""
    current_state = await state.get_state()

    if current_state == "DiscogsFSM:discogs_state":
        await state.update_data(discogs_state=True)
    else:
        await state.clear()
        await bot.send_message(
            chat_id=message.chat.id,
            text="Просмотр завершен...",
            reply_markup=ReplyKeyboardRemove(),
        )
        await message.answer(
            "Просмотр музыкальных альбомов для сайта discogs.com завершен",
            reply_markup=get_main_menu_button(),
        )


@router.message(DiscogsFSM.discogs_state, F.text)
@router.message(DiscogsFSM.albums_list, F.text)
async def get_message_DiscogsFSM(message: Message, state: FSMContext):
    """Отправляет пользователю сообщение если он написал при обработке запроса на получение альбомов."""
    current_state = await state.get_state()

    if current_state == "DiscogsFSM:discogs_state":
        await message.answer(text="Дождитесь обработки запроса или нажмите 'Отмена'")
    else:
        await message.answer(text="Нажмите кнопку 'Отмена' выйти в меню")


@router.callback_query(StateFilter(None), F.data.startswith("GenreDiscogs_"))
async def get_album_artists_by_genre_for_site_discogs(
    call: CallbackQuery,
    state: FSMContext,
):
    """Возвращает найденных исполнителей для discogs и кнопки назад и вперед."""
    _, genre = call.data.split("_")

    await call.message.delete_reply_markup()

    year: int = datetime.now().year

    # Функция нужна для того если пользователь нажмет Отмена
    def cancel_check() -> bool:
        """Возвращает статус состояния отмены FSM DiscogsFSM

        Returns:
            _type_: Возвращает статус состояния отмены FSM DiscogsFSM
        """
        data: Dict = asyncio.run_coroutine_threadsafe(state.get_data(), loop).result()
        return data.get("discogs_state", False)

    # Встаем в discogs_state для того чтобы пользователь ожидал загрузки и ни куда не мог перейти
    await state.set_state(DiscogsFSM.discogs_state)

    loop = asyncio.get_event_loop()

    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Процесс начался...",
        reply_markup=get_cancel_button(),
    )
    progress_msg: Message = await call.message.answer("⏳ Обработка")
    # 🧠 Передача аргументов в run_in_executor
    processing_task: Future[List] = loop.run_in_executor(
        None,
        get_list_albums_for_discogs,
        genre,
        50,
        discogs_setting.URL_SEARCH,
        year,
        cancel_check,
    )

    # Анимация загрузки
    dots: List = ["", ".", "..", "..."]
    dot_index: 0 = 0

    while not processing_task.done():
        data = await state.get_data()

        if data.get("discogs_state", None):
            break
        try:
            await progress_msg.edit_text(f"⏳ Обработка{dots[dot_index % len(dots)]}")
        except Exception:
            pass
        dot_index += 1
        await asyncio.sleep(0.5)

    data: Dict = await state.get_data()
    if data.get("discogs_state", None):

        await bot.send_message(chat_id=call.message.chat.id, text="Подождите идет процесс отмены обработки...")

        # Ждем пока отменятся все таски чтобы корректно сделать state.clear
        while not processing_task.done():
            await bot.send_chat_action(call.message.chat.id, "typing")
            await asyncio.sleep(0.5)

        await state.clear()
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="Обработка прервана...",
            reply_markup=ReplyKeyboardRemove(),
        )
        await call.message.answer(
            "Обработка выдачи альбомов музыкальных "
            "исполнителей для сайта discogs.com прервана",
            reply_markup=get_main_menu_button(),
        )
        return
    else:
        try:
            data = await processing_task

            album_artist: Dict = data[0].dict()
            img: str = album_artist["IMG"]

            album: str = get_descripions_for_albums(album_artist)
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=img,
                caption=album,
                reply_markup=get_button_for_forward_or_back(
                    list_albums=album_artist, count=0, step=1
                ),
            )
            await state.set_state(DiscogsFSM.albums_list)
            await state.update_data(albums_list=data)
        except Exception as e:
            # 👇 Обрабатываем ошибку
            await progress_msg.edit_text(
                f"❌ Произошла ошибка при обработке:\n`{str(e)}`"
            )


@router.callback_query(DiscogsFSM.albums_list, F.data.startswith("discogs "))
async def leafing_through_albums(call: CallbackQuery, state: FSMContext):
    """Листает альбомы назад и вперед."""
    _, button, count = call.data.split(" ")

    data: Dict = await state.get_data()
    albums_list: List = data["albums_list"]
    album: Dict = albums_list[int(count)].dict()
    img: str = album["IMG"]
    description_album: str = get_descripions_for_albums(album)

    with open("file.txt", "w", encoding="utf-8") as file:
        file.write(description_album)

    await bot.edit_message_media(
        media=InputMediaPhoto(media=img, caption=description_album),
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=get_button_for_forward_or_back(
            count=int(count),
            list_albums=albums_list,
        ),
    )
