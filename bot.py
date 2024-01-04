import telebot, database as db, buttons as bt
from geopy import Nominatim

# Создать объект бота
bot = telebot.TeleBot('6825008876:AAEN-AxrvVEIOg4SVnVuRdtKCMPn6Ogq45Q')
# Использование карт
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')


# Обработка команды start
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    # Проверка пользователя
    check = db.checker(user_id)
    if check:
        bot.send_message(user_id, f'Добро пожаловать, {message.from_user.first_name}!')
    else:
        bot.send_message(user_id, "Здравствуйте, добро пожаловать! Давайте начнем "
                                  "регистрацию, введите свое имя!")
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)


# Этап получения имени
def get_name(message):
    name = message.text
    user_id = message.from_user.id
    bot.send_message(user_id, "Отлично, а теперь отправьте номер!",
                     reply_markup=bt.num_bt())
    # Этап получения номера
    bot.register_next_step_handler(message, get_number, name)


# Этап получения номера
def get_number(message, name):
    user_id = message.from_user.id
    # Если юзер отправил номер по кнопке
    if message.contact:
        number = message.contact.phone_number
        bot.send_message(user_id, 'Супер! Последний этап: отправь локацию',
                         reply_markup=bt.loc_bt())
        # Этап получения локации
        bot.register_next_step_handler(message, get_location, name, number)
    # Если юзер отправил номер не по кнопке
    else:
        bot.send_message(user_id, 'Отправьте номер через кнопку',
                         reply_markup=bt.num_bt())
        # Этап получения номера
        bot.register_next_step_handler(message, get_number, name)

# Этап получения локации
def get_location(message, name, number):
    user_id = message.from_user.id
    # Если юзер отправил локацию по кнопке
    if message.location:
        location = str(geolocator.reverse(f'{message.location.latitude}, '
                                      f'{message.location.longitude}'))
        db.register(user_id, name, number, location)
        bot.send_message(user_id, 'Регистрация прошла успешно',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    # Если юзер отправил локацию не по кнопке
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку',
                         reply_markup=bt.loc_bt())
        # Этап получения номера
        bot.register_next_step_handler(message, get_location, name, number)


# Запуск бота
bot.polling(non_stop=True)

