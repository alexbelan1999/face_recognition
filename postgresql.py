import datetime

import psycopg2


def insert(persons: list):
    exit = True
    connection = None
    try:

        connection = psycopg2.connect(dbname='testdb', user='postgres', password='1234', host='127.0.0.1')
        with connection.cursor() as cursor:
            for person in persons:
                sql = "INSERT INTO public.persons (name, addtime) VALUES ('" + person[0] + "', '" + person[1] + "');"
                cursor.execute(sql)
            connection.commit()
            cursor.close()


    except psycopg2.OperationalError:
        print("Ошибка соединения с базой данных!")
        exit = False

    finally:
        if exit == True:
            connection.close()


def select_all():
    exit = True
    connection = None

    try:
        sql = "SELECT id, name , addtime from persons;"
        connection = psycopg2.connect(dbname='testdb', user='postgres', password='1234', host='127.0.0.1')
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                print("Id: ", row[0], " Имя: ", row[1], " Время: ", row[2])
            connection.commit()
            cursor.close()


    except psycopg2.OperationalError:
        print("Ошибка соединения с базой данных!")
        exit = False

    finally:
        if exit == True:
            connection.close()


select_all()
