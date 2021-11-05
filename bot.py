import os
import processing
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

API_KEY = os.getenv('API_KEY')


class ImageProc(StatesGroup):
    choosing = State()
    return_img = State()


logging.basicConfig(level=logging.INFO)

bot = Bot(API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'], state=None)
async def start_message(message: types.Message):
    await message.answer(
        'Привет \U0001F44B ! Я могу помочь тебе обработать твоё изображение! Присылай изображение и выбирай фильтр.\n\n'
        'Доступные фильтры: \n'
        '1. Серое изображение.\n'
        '2. Заблюренное изображение.\n'
        '3. Добавить яркость.\n'
        '4. Убавить яркость.\n')


@dp.message_handler(commands=['help'], state=None)
async def start_message(message: types.Message):
    await message.answer('Присылай изображение и выбирай фильтр!\n\n'
                         'Доступные фильтры: \n'
                         '1. Серое изображение.\n'
                         '2. Заблюренное изображение.\n'
                         '3. Добавить яркость.\n'
                         '4. Убавить яркость.\n')


@dp.message_handler(commands=['new'], state=None)
async def new_message(message: types.Message):
    await message.answer('Можете присылать изображение', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=['photo'], state=None)
async def get_img(message: types.Message):
    await message.photo[-1].download(destination_file='photos/photo_{}.jpg'.format(message.from_user.id))
    # await message.answer('da',reply_markup=ReplyKeyboardRemove())
    await ImageProc.choosing.set()
    await choosing_filter(message)


@dp.message_handler(state=ImageProc.choosing)
async def choosing_filter(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_gray = KeyboardButton('Серое изображение')
    button_blur = KeyboardButton('Заблюренное изображение')
    button_add = KeyboardButton('Добавить яркость')
    button_sub = KeyboardButton('Убавить яркость')
    # buttons = ['Серое изображение', 'Заблюренное изображение', 'Добавить яркости', 'Убавить яркости']
    # keyboard.add(*buttons)
    keyboard.row(button_gray, button_blur)
    keyboard.row(button_add, button_sub)
    await message.answer('Выберите фильтр', reply_markup=keyboard)
    await ImageProc.return_img.set()


@dp.message_handler(content_types=['any'], state=ImageProc.return_img)
async def send_img(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    load_img = False

    if message.text == 'Серое изображение':
        img = processing.read_img(user_id)
        processing.save_img(processing.get_grayscale_img(img), user_id)
        load_img = True
    elif message.text == 'Заблюренное изображение':
        img = processing.read_img(user_id)
        processing.save_img(processing.get_blur_img(img), user_id)
        load_img = True
    elif message.text == 'Добавить яркость':
        img = processing.read_img(user_id)
        processing.save_img(processing.get_add_bright_img(img), user_id)
        load_img = True
    elif message.text == 'Убавить яркость':
        img = processing.read_img(user_id)
        processing.save_img(processing.get_sub_bright_img(img), user_id)
        load_img = True

    if load_img == True:
        result = types.InputFile('photos/result_{}.jpg'.format(user_id))

        await bot.send_photo(message.from_user.id, result, reply_markup=ReplyKeyboardRemove())
        os.remove('photos/photo_{}.jpg'.format(user_id))
        os.remove('photos/result_{}.jpg'.format(user_id))
        await state.finish()
    else:
        await message.answer('Если что-то пошло не так, наберите /new')
        await state.finish()


# run long-polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
