import psycopg2
from pprint import pprint

self_database = 'userdata'
self_user = 'postgres'
self_password = 'data_base'


def drop_table(cursor):
    cursor.execute("""
    DROP TABLE phones;
    DROP TABLE users;
    """)


def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(40) NOT NULL, 
        last_name VARCHAR(40) NOT NULL, 
        email VARCHAR(30) UNIQUE NOT NULL 
        );

        CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY, 
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        phone_number VARCHAR(25)
        );
    """)
    print('Созданы таблицы "users" и "phones"')


def add_new_user(cursor, user_first_name, user_last_name, user_email):
    cursor.execute("""
        INSERT INTO users(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id, first_name;
        """, (user_first_name, user_last_name, user_email))
    print(cursor.fetchone())


def add_phone_number(cursor, id_user, number):
    cursor.execute("""
        INSERT INTO phones(user_id, phone_number) VALUES(%s, %s);
        """, (id_user, number))
    print(f'Пользователю с id {id_user} добавлен телефон {number}')


def change_user_info(cursor):
    print('Какую информацию вы хотите изменить?\n'
          '1 - Смена имени\n'
          '2 - Смена фамилии\n'
          '3 - Смена email\n'
          '4 - Смена телефона\n'
          '5 - Отмена')
    answer = int(input())
    if answer == 1:
        id_of_user = int(input('Введите id пользователя: '))
        new_name = input('Введите новое имя: ')
        cursor.execute("""
            UPDATE users SET first_name = %s WHERE id = %s;
            """, (new_name, id_of_user))
        print(f'Имя изменено на {new_name}')
        question = input('Хотите изменить что-нибудь еще? да/нет\n'
                         '')
        if question.lower() == 'да':
            change_user_info(cursor)
        else:
            pass
    elif answer == 2:
        id_of_user = int(input('Введите id пользователя: '))
        new_surname = input('Введите новую фамилию: ')
        cursor.execute("""
            UPDATE users SET last_name = %s WHERE id = %s;
            """, (new_surname, id_of_user))
        print(f'Фамилия изменена на {new_surname}')
        question = input('Хотите изменить что-нибудь еще? да/нет\n'
                         '')
        if question.lower() == 'да':
            change_user_info(cursor)
        else:
            pass
    elif answer == 3:
        id_of_user = int(input('Введите id пользователя: '))
        new_email = input('Введите новый email: ')
        cursor.execute("""
            UPDATE users SET email = %s WHERE id = %s;
            """, (new_email, id_of_user))
        print(f'Email изменен на {new_email}')
        question = input('Хотите изменить что-нибудь еще? да/нет\n'
                         '')
        if question.lower() == 'да':
            change_user_info(cursor)
        else:
            pass
    elif answer == 4:
        id_of_user = int(input('Введите id пользователя: '))
        cursor.execute("""
                SELECT phone_number FROM phones WHERE user_id=%s;
                """, (id_of_user,))
        print(cursor.fetchall())
        pre_number = input('Введите номер который хотите заменить: ')
        new_number = input('Введите новый телефон: ')
        cursor.execute("""
            UPDATE phones SET phone_number = %s WHERE phone_number = %s;
            """, (new_number, pre_number))
        print(f'Телефон {pre_number} изменен на {new_number}')
        question = input('Хотите изменить что-нибудь еще? да/нет\n'
                         '')
        if question.lower() == 'да':
            change_user_info(cursor)
        else:
            pass
    else:
        pass


def delete_phone_number(cursor, id_of_user):
    cursor.execute("""
                SELECT phone_number FROM phones WHERE user_id=%s
                """, (id_of_user,))
    numbers_for_delete = cursor.fetchall()
    print(numbers_for_delete)
    if numbers_for_delete:
        del_number = input('Введите номер который хотите удалить:')
        for number in numbers_for_delete:
            if del_number in number:
                cursor.execute("""
                    DELETE FROM phones WHERE user_id = %s and phone_number = %s
                    """, (id_of_user, del_number))
                print(f'Номер {del_number} удален')
            else:
                print('У пользователя нет такого номера.')
    else:
        print('Нет номера для удаления.')


def delete_user(cursor, id_of_user):
    cursor.execute("""
        DELETE FROM users WHERE id = %s
        """, (id_of_user, ))
    print(f'Пользователь с id {id_of_user} удален.')


def find_user(cursor, user_name=None, user_surname=None, user_email=None, user_number=None):
    cursor.execute("""
        select first_name, last_name, email, phone_number from users u 
        full join phones p on p.user_id = u.id 
        WHERE first_name SIMILAR TO %s or last_name SIMILAR TO %s or email SIMILAR TO %s or 
        phone_number SIMILAR TO %s;
        """, (user_name, user_surname, user_email, user_number))
    pprint(cursor.fetchall())


if __name__ == "__main__":
    with psycopg2.connect(database='userdata', user='postgres', password='data_base') \
            as connection:
        with connection.cursor() as cur:
            drop_table(cur)
            create_table(cur)
            add_new_user(cur, 'Pavel', 'Durov', 'pav.dur@gmai.con')
            add_new_user(cur, 'Bill', 'Gates', 'bill.gat@ya.con')
            add_new_user(cur, 'Bill', 'Phone', 'ott.p@ya.con')
            add_phone_number(cur, 1, '8-800-555-36-32')
            add_phone_number(cur, 1, '8-800-00')
            add_phone_number(cur, 2, '555')
            change_user_info(cur)
            delete_phone_number(cur, 2)
            delete_user(cur, 6)
            find_user(cur, user_surname='Gates')

    connection.close()



