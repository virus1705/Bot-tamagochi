import sqlite3
import logging


DB_DIR = 'db'
DB_NAME = 'db.sqlite'
DB_TABLE_USERS_NAME = 'users'
table_name = 'tamagochi'


# Функция для выполнения любого sql-запроса для изменения данных
def execute_query(db_file, query, data=None):
    """
    Функция для выполнения запроса к базе данных.
    Принимает имя файла базы данных, SQL-запрос и опциональные данные для вставки.
    """

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)

    connection.commit()
    connection.close()


#создание таблицы
def prepare_database():
    sql_query = f'CREATE TABLE IF NOT EXISTS {table_name} ' \
                    f'(id INTEGER PRIMARY KEY, ' \
                    f'user_id INTEGER, ' \
                    f'data_create TEXT, ' \
                    f'data_eating TEXT, ' \ 
                    f'data_sleep TEXT, ' \
                    f'data_play TEXT, ' \
                    f'pet BLOB)'
    #если надо добавить что-то ещё - напишите
    execute_query(DB_NAME, sql_query)

# Функция для выполнения любого sql-запроса для получения данных (возвращает значение)
def sending_request(sql_query, data=None, db_path=f'{DB_NAME}'):
    try:
        logging.info(f"DATABASE: Execute query: {sql_query}")

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        if data:
            cursor.execute(sql_query, data)
        else:
            cursor.execute(sql_query)

        rows = cursor.fetchall()
        connection.close()
        return rows

    except sqlite3.Error as e:
        logging.error(f"DATABASE: Ошибка при запросе: {e}")
        print("Ошибка при выполнении запроса:", e)



#добавление нового пользователя. pet - кто является питомцем(кролик например), data_create - дата создания
def insert_data(user_id, data_create, pet):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    query = f'''INSERT INTO {table_name} (user_id,data_create, pet) VALUES (?, ?, ?)'''
    cur.execute(query, (user_id, data_create, pet))
    con.close()

#----------------------------------------обновление данных-----------------------------------------------------

#запрос к SQL по критериям
def update_data(user_id, column, value):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    #column - название поля в таблице users
    query = f'UPDATE {table_name} SET {column} = ? WHERE user_id = ?'
    cur.execute(query, (user_id, value, ))
    con.commit()
    con.close()

#обновление данных о дате создания
def update_data_create(user_id, data_create):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    #column - название поля в таблице users
    query = f'UPDATE {table_name} SET data_create = {data_create} WHERE user_id = ?'
    cur.execute(query, (user_id, ))
    con.commit()
    con.close()

#обновление данных о дате сна питомца
def update_data_sleep(user_id, data_sleep):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    #column - название поля в таблице users
    query = f'UPDATE {table_name} SET data_sleep = {data_sleep} WHERE user_id = ?'
    cur.execute(query, (user_id, ))
    con.commit()
    con.close()

#обновление данных о дате игры с питомцем
def update_data_play(user_id, data_play):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    query = f'UPDATE {table_name} SET data_play = {data_play} WHERE user_id = ?'
    cur.execute(query, (user_id, ))
    con.commit()
    con.close()

#обновление данных о том, кто является питомцем
def update_data_pet(user_id, pet):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    query = f'UPDATE {table_name} SET pet = {pet} WHERE user_id = ?'
    cur.execute(query, (user_id, ))
    con.commit()
    con.close()

#обновление данных о дате кормления питомца
def update_data_eating(user_id, data_eating):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    #column - название поля в таблице users
    query = f'UPDATE {table_name} SET data_eating = {data_eating} WHERE user_id = ?'
    cur.execute(query, (user_id, ))
    con.commit()
    con.close()

#--------------------------------------получение информации------------------------------------------------------------
#получение информации о том, кто является питомцем пользователя
def get_user_pet(user_id):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    query = f'SELECT pet FROM {table_name} WHERE user_id = {user_id}'
    cur.execute(query)

    rows = cur.fetchall()
    con.close()
    return rows

# #получение информации о имени питомца
# def get_user_pet_name(user_id):
#     con = sqlite3.connect('db.sqlite')
#     cur = con.cursor()
#
#     query = f'SELECT pet_name FROM {table_name} WHERE user_id = {user_id}'
#     cur.execute(query)
#
#     rows = cur.fetchall()
#     con.close()
#     return rows

#получение информации о дате рождения питомца
def get_user_pet_data_create(user_id):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    query = f'SELECT data_create FROM {table_name} WHERE user_id = {user_id}'
    cur.execute(query)

    rows = cur.fetchall()
    con.close()
    return rows

#получение информации о дате сна питомца
def get_user_pet_data_sleep(user_id):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    query = f'SELECT data_sleep FROM {table_name} WHERE user_id = {user_id}'
    cur.execute(query)

    rows = cur.fetchall()
    con.close()
    return rows

#получение информации о дате игры с питомцем
def get_user_pet_data_play(user_id):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    query = f'SELECT data_play FROM {table_name} WHERE user_id = {user_id}'
    cur.execute(query)

    rows = cur.fetchall()
    con.close()
    return rows

#получение информации о дате кормления
def get_user_pet_data_eating(user_id):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    query = f'SELECT data_eating FROM {table_name} WHERE user_id = {user_id}'
    cur.execute(query)

    rows = cur.fetchall()
    con.close()
    return rows