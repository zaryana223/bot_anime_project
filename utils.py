from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

# Функция для создания клавиатуры с кнопкой "ТОП-10 техник по популярности"
def get_kb():
    btns = [
        ['ТОП-10 техник по популярности'],
    ]
    return ReplyKeyboardMarkup(btns, resize_keyboard=True)

# Функция для создания клавиатуры с кнопками, выдающими техники
def get_techs_kb(techs):
    btns = []
    for t in techs:
        # Создаем кнопку с текстом техники и callback_data равным ее id в БД
        # Так сделано, потому что названия некоторых техник слишком тяжелые для инлайн-кнопок,
        # поэтому пришлось заменить callback data на id из базы
        btns.append([InlineKeyboardButton(t.name, callback_data=str(t.id))])
    return InlineKeyboardMarkup(btns)
