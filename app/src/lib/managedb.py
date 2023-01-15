import peewee
from collections import Counter
import pymysql
import pandas as pd
from decouple import config
import json


HOST_MYSQL = config('HOST_MYSQL')
PORT_MYSQL = int(config('PORT_MYSQL'))
USER_MYSQL = config('USER_MYSQL')
PASSWORD_MYSQL = config('PASSWORD_MYSQL')
DB_MYSQL = config('DB_MYSQL')

database = peewee.MySQLDatabase(
    DB_MYSQL,
    host=HOST_MYSQL,
    port=PORT_MYSQL,
    user=USER_MYSQL,
    passwd=PASSWORD_MYSQL
)

# Creación de la Tabla


class Movies(peewee.Model):
    show_id = peewee.PrimaryKeyField()
    type = peewee.CharField(max_length=50)
    title = peewee.CharField(max_length=100)
    director = peewee.CharField(max_length=50)
    cast = peewee.CharField(max_length=300)
    country = peewee.CharField(max_length=100)
    date_added = peewee.CharField(max_length=200)
    release_year = peewee.IntegerField()
    rating = peewee.CharField(max_length=10)
    duration = peewee.IntegerField()
    listed_in = peewee.CharField(max_length=50)
    description = peewee.CharField(max_length=500)
    platform = peewee.CharField(max_length=50)

    class Meta:
        database = database
        db_table = DB_MYSQL


def create_database_if_not_exists(host, user, password, db_name):
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = connection.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
        result = cursor.fetchone()
        if result:
            print(f"La base de datos {db_name} ya existe.")
        else:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"La base de datos {db_name} fue creada exitosamente.")
    except pymysql.Error as error:
        print(f"Ocurrió un error al verificar/crear la base de datos: {error}")
    finally:
        connection.close()


def upload_data_to_mysql(tb_model, file_name):
    try:
        # Verificar si la tabla existe y eliminarla si es necesario
        if tb_model.table_exists():
            tb_model.drop_table()
        # Crear tabla en MySQL
        tb_model.create_table()

        # Abrir archivo json y cargar los datos en una variable
        # app/src/db/movies.json
        with open(f'app/src/db/{file_name}.json') as file:
            data = json.load(file)

        # Insertar los datos en la tabla
        query = tb_model.insert_many(data)
        query.execute()

        print(f'Carga de "{file_name}.json" completado Exitosamente!!')
    except Exception as e:
        print(f"Ocurrió un error al cargar los datos: {e}")


if __name__ == '__main__':
    create_database_if_not_exists(HOST_MYSQL, USER_MYSQL, PASSWORD_MYSQL, DB_MYSQL)
    upload_data_to_mysql(Movies, DB_MYSQL)
