from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Place Order"), KeyboardButton("Ask about Availability"), KeyboardButton("Ask a question"))
    return keyboard