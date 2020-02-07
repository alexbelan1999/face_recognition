import psycopg2


def insert(pname, time):
    exit = True
    connection = None
    try:
        print("Загрузка данных на сервер.")
        sql = "INSERT INTO public.persons (name, addtime) VALUES ('" + pname + "', '" + time + "');"

        connection = psycopg2.connect(dbname='testdb', user='postgres', password='1234', host='127.0.0.1')
        with connection.cursor() as cursor:

            cursor.execute(sql)
            connection.commit()
            cursor.close()


    except psycopg2.OperationalError:
        print("Ошибка соединения с базой данных!")
        exit = False

    finally:
        if exit == True:
            connection.close()
            print("Соединение закрыто")
