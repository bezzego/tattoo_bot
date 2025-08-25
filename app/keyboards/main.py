from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app import texts


def main_menu():
    buttons = [
        [KeyboardButton(text=texts.MENU_CALCULATE)],
        [KeyboardButton(text=texts.MENU_PORTFOLIO)],
        [KeyboardButton(text=texts.MENU_REVIEWS)],
        [KeyboardButton(text=texts.MENU_HEALING)],
        [KeyboardButton(text=texts.MENU_CONTACT)],
        [KeyboardButton(text=texts.MENU_SKETCHES)],
        [KeyboardButton(text=texts.MENU_ABOUT)],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
