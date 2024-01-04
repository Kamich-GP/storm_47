import sqlite3

# Подключение к БД
connection = sqlite3.connect("shop.db", check_same_thread=False)
# Python + SQL
sql = connection.cursor()


## Создание таблиц ##
# Таблица пользователей
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(id INTEGER, name TEXT, number TEXT, location TEXT);')
# Таблица продуктов
sql.execute('CREATE TABLE IF NOT EXISTS products '
            '(id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT,'
            'pr_des TEXT, pr_count INTEGER, pr_photo TEXT, pr_price REAL);')
# Таблица корзины
sql.execute('CREATE TABLE IF NOT EXISTS cart '
            '(user_id INTEGER, user_product TEXT, pr_amount INTEGER, total REAL);')


## Методы для пользователя ##
# Регистрация
def register(id, name, number, location):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (id, name, number, location))
    # Фиксируем изменения
    connection.commit()


# Проверка на наличие пользователя в БД
def checker(id):
    check = sql.execute('SELECT id FROM users WHERE id=?;', (id,))

    if check.fetchone():
        return True
    else:
        return False

