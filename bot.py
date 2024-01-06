import telebot, database as db, buttons as bt
from geopy import Nominatim

# Создать объект бота
bot = telebot.TeleBot('6815759762:AAEtxvJNQ6L41kiqTOaTeQ1kWhE-Zz63A0c')
# Использование карт
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')


# Обработка команды start
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    print(user_id)
    # Проверка пользователя
    check = db.checker(user_id)
    if check:
        bot.send_message(user_id, f'Добро пожаловать, {message.from_user.first_name}!',)
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
        products = db.get_pr_but()
        bot.send_message(user_id, 'Регистрация прошла успешно',
                         reply_markup=bt.main_menu_buttons(products))
    # Если юзер отправил локацию не по кнопке
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку',
                         reply_markup=bt.loc_bt())
        # Этап получения номера
        bot.register_next_step_handler(message, get_location, name, number)


# Обработка команды admin
@bot.message_handler(commands=['admin'])
def act(message):
    admin_id = 6775701667
    if message.from_user.id == admin_id:
        bot.send_message(admin_id, 'Выберите действие', reply_markup=bt.admin_menu())
        # Переход на этап выбора
        bot.register_next_step_handler(message, admin_choose)
    else:
        bot.send_message(message.from_user.id, 'Вы не админ!')

# Выбор действия админом
def admin_choose(message):
    admin_id = 6775701667
    if message.text == 'Добавить продукт':
        bot.send_message(admin_id, 'Напишите название продукта!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения названия
        bot.register_next_step_handler(message, get_pr_name)
    elif message.text == 'Удалить продукт':
        bot.send_message(admin_id, 'Напишите id продукта!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения названия
        bot.register_next_step_handler(message, get_pr_id)
    elif message.text == 'Изменить продукт':
        bot.send_message(admin_id, 'Напишите id продукта!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения названия
        bot.register_next_step_handler(message, get_pr_change)
    elif message.text == 'Перейти в меню':
        products = db.get_pr_but()
        bot.send_message(admin_id, 'Добро пожаловать в меню!',
                         reply_markup=bt.main_menu_buttons(products))
    else:
        bot.send_message(admin_id, 'Неизвестная операция', reply_markup=bt.admin_menu())
        # Возврат на этап выбора
        bot.register_next_step_handler(message, admin_choose)

# Запуск бота
bot.polling(non_stop=True)

