from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_quote_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Начнем", callback_data="start_quote")]
        ]
    )


def zone_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Рука (плечо)", callback_data="zone:shoulder")],
            [
                InlineKeyboardButton(
                    text="Рука (предплечье)", callback_data="zone:forearm"
                )
            ],
            [InlineKeyboardButton(text="Нога", callback_data="zone:leg")],
            [InlineKeyboardButton(text="Спина", callback_data="zone:back")],
            [InlineKeyboardButton(text="Грудь", callback_data="zone:chest")],
            [InlineKeyboardButton(text="Другое", callback_data="zone:other")],
        ]
    )


def idea_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Да, есть изображение", callback_data="idea:image"
                )
            ],
            [InlineKeyboardButton(text="Нет, нужна помощь", callback_data="idea:help")],
            [
                InlineKeyboardButton(
                    text="Да, хочу индивидуальный эскиз", callback_data="idea:custom"
                )
            ],
        ]
    )


def size_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="до 10 см", callback_data="size:small")],
            [InlineKeyboardButton(text="11–20 см", callback_data="size:medium")],
            [InlineKeyboardButton(text="большая площадь", callback_data="size:large")],
        ]
    )


def work_type_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Новая тату", callback_data="work:new"),
                InlineKeyboardButton(text="Перекрытие", callback_data="work:cover"),
            ],
        ]
    )


def done_refs_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Готово", callback_data="refs_done")],
        ]
    )


def confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Отправить заявку", callback_data="send_app"
                )
            ],
        ]
    )


def toggle_leads_keyboard(current_state: bool):
    text = "Выключить приём заявок" if current_state else "Включить приём заявок"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data="toggle_leads")],
        ]
    )
