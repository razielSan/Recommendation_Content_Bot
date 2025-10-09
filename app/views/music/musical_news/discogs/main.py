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
from utils.music.discogs.discogs import make_update_progress, make_cancel_check


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
    counter = State()


@router.message(DiscogsFSM.counter, F.text == "Отмена")
@router.message(DiscogsFSM.albums_list, F.text == "Отмена")
async def cancel_discogs_handler(message: Message, state=FSMContext):
    """Работа с FSM DiscogsFSM.Отменяет все действия."""
    current_state = await state.get_state()

    if current_state == "DiscogsFSM:counter":
        await state.set_state(DiscogsFSM.discogs_state)
        await state.update_data(discogs_state=True)
        await state.set_state(DiscogsFSM.counter)
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


@router.message(DiscogsFSM.counter, F.text)
@router.message(DiscogsFSM.albums_list, F.text)
async def get_message_DiscogsFSM(message: Message, state: FSMContext):
    """Отправляет пользователю сообщение если он написал при обработке запроса на получение альбомов."""
    current_state = await state.get_state()

    if current_state == "DiscogsFSM:counter":
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

    digit: int = discogs_setting.COUNT_ALBUMS_SEARCH

    # Встаем в discogs_state для того чтобы пользователь ожидал загрузки и ни куда не мог перейти
    await state.set_state(DiscogsFSM.counter)
    await state.update_data(counter=0)

    loop = asyncio.get_event_loop()

    # Функция для отслеживания прогресса обработки скачивания информации об альбомах
    update_pogress = make_update_progress(loop=loop, state=state)

    # Функция для отмены скачивания информации об альбомах при нажатии пользователем кнопки Отмена
    cancel_check = make_cancel_check(loop=loop, state=state)

    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Процесс начался...",
        reply_markup=get_cancel_button(),
    )
    progress_msg: Message = await call.message.answer(
        f"👩‍🔬 Обработка запроса:\n\n📥 " f"Скачивание альбомов: 0%"
    )
    # 🧠 Передача аргументов в run_in_executor
    processing_task: Future[List] = loop.run_in_executor(
        None,
        get_list_albums_for_discogs,
        genre,
        digit,
        discogs_setting.URL_SEARCH,
        year,
        cancel_check,
        update_pogress,
    )

    while not processing_task.done():
        data = await state.get_data()

        if data.get("discogs_state", None):
            break
        try:
            result = (data.get("counter", 0) / digit) * 100
            await progress_msg.edit_text(
                f"👩‍🔬 Обработка запроса:\n\n📥 " f"Скачивание альбомов: {result:.1f}%"
            )
        except Exception:
            pass
        await asyncio.sleep(0.5)

    data: Dict = await state.get_data()
    if data.get("discogs_state", None):

        await bot.send_message(
            chat_id=call.message.chat.id,
            text="Подождите идет процесс отмены обработки...",
        )

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

            # Ставим на засыпание чтобы пользователь сперва увидел сообщение о загрузке
            await progress_msg.edit_text(
                "👩‍🔬 Обработка запроса:\n\n✅ Альбомы загружены"
            )
            await asyncio.sleep(1)

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
