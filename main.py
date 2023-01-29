import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import menu_keyboard


load_dotenv()

bot_token = os.getenv('TELEGRAM_TOKEN')

# bot inicialization
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Create a states group for the state machine
class MenuStates(StatesGroup):
    waiting_for_command = State()


class Order(StatesGroup):
    waiting_for_product_name = State()
    waiting_for_product_amount = State()


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer("Hello "+user_name+"! Please select an option:", reply_markup=menu_keyboard())


@dp.message_handler(Text(equals=('Place Order'), ignore_case=True), state=None)
async def add_expense(message: types.Message) -> None:
    await Order.waiting_for_product_name.set()
    await message.answer(text='Enter name of desired product')


@dp.message_handler(state=Order.waiting_for_product_name)
async def order_processing_product_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["product_name"] = message.text  # Add availibility check
    await state.finish()
    await Order.waiting_for_product_amount.set()
    await message.reply(text='Now, enter desired amount')


@dp.message_handler(state=Order.waiting_for_product_amount)
async def order_processing_product_amount(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["product_amount"] = message.text
    await state.finish()
    await MenuStates.waiting_for_command.set()


@dp.message_handler(state=MenuStates.waiting_for_command)
async def menu(message: types.Message) -> None:
    await message.answer("Please select an option", reply_markup=menu_keyboard())

if __name__ == '__main__':
    executor.start_polling(dp)
