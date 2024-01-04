from telebot import types


# Кнопка для отправки номера
def num_bt():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    number = types.KeyboardButton('Отправить номер', request_contact=True)
    # Добавляем кнопки в пространство
    kb.add(number)
    return kb


# Кнопка для отправки локации
def loc_bt():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    location = types.KeyboardButton('Отправить локацию', request_location=True)
    # Добавляем кнопки в пространство
    kb.add(location)
    return kb

