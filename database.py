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


## Методы для продуктов ##
# Вывод инфы о конкретном товаре
def get_pr(id):
    result = sql.execute('SELECT pr_name, pr_des, pr_count, pr_photo, pr_price FROM products WHERE id=?;',
                         (id,))
    return result.fetchone()

# Метод для отображения продуктов в кнопках
def get_pr_but():
    return sql.execute('SELECT id, pr_name, pr_count FROM products;').fetchall()


# Метод для добавления продукта в БД
def add_pr(name, des, count, photo, price):
    sql.execute('INSERT INTO products(pr_name, pr_des, pr_count, pr_photo, pr_price) '
                'VALUES(?, ?, ?, ?, ?);', (name, des, count, photo, price))
    # Фиксируем изменения
    connection.commit()

# Метод для удаления
def del_pr(id):
    sql.execute('DELETE FROM products WHERE id=?;', (id,))
    # Фиксируем изменения
    connection.commit()

# Метод для изменения количества
def change_pr_count(id, new_count):
    # Текущее кол-во товара
    now_count = sql.execute('SELECT pr_count WHERE id=?;', (id,)).fetchone()
    # Приход товара
    plus_count = now_count[0] + new_count
    sql.execute('UPDATE products SET pr_count=? WHERE id=?;', (plus_count, id))
    # Фиксируем изменения
    connection.commit()


## Методы корзины ##
def add_pr_to_cart(user_id, user_product, pr_amount, total):
    sql.execute('INSERT INTO cart VALUES(?, ?, ?, ?);', (user_id, user_product, pr_amount, total))
    # Фиксируем изменения
    connection.commit()

