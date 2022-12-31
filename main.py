import peewee
import pandas as pd
from decouple import config
import json


HOST_MYSQL=config('HOST_MYSQL')
PORT_MYSQL=int(config('PORT_MYSQL'))
USER_MYSQL=config('USER_MYSQL')
PASSWORD_MYSQL = config('PASSWORD_MYSQL')
DB_MYSQL = config('DB_MYSQL')

database = peewee.MySQLDatabase(
    DB_MYSQL,
    host=HOST_MYSQL,
    port=PORT_MYSQL,
    user=USER_MYSQL,
    passwd=PASSWORD_MYSQL
)

# Creación de las tablas

class AmazonPrime(peewee.Model):
    show_id = peewee.PrimaryKeyField()
    type = peewee.CharField(max_length=50)
    title = peewee.CharField(max_length=100)
    director = peewee.CharField(max_length=50)
    cast = peewee.CharField(max_length=300)
    country = peewee.CharField(max_length=100)
    date_added = peewee.DateTimeField()
    release_year = peewee.IntegerField()
    rating = peewee.CharField(max_length=10)
    duration = peewee.CharField(max_length=10)
    listed_in = peewee.CharField(max_length=50)
    description = peewee.CharField(max_length=500)
    class Meta:
        database = database
        db_table = 'amazon_movies'

class DisneyPlus(peewee.Model):
    show_id = peewee.PrimaryKeyField()
    type = peewee.CharField(max_length=50)
    title = peewee.CharField(max_length=100)
    director = peewee.CharField(max_length=50)
    cast = peewee.CharField(max_length=300)
    country = peewee.CharField(max_length=100)
    date_added = peewee.DateTimeField()
    release_year = peewee.IntegerField()
    rating = peewee.CharField(max_length=10)
    duration = peewee.CharField(max_length=10)
    listed_in = peewee.CharField(max_length=50)
    description = peewee.CharField(max_length=500)
    class Meta:
        database = database
        db_table = 'disney_movies'

class Hulu(peewee.Model):
    show_id = peewee.PrimaryKeyField()
    type = peewee.CharField(max_length=50)
    title = peewee.CharField(max_length=100)
    director = peewee.CharField(max_length=50)
    cast = peewee.CharField(max_length=300)
    country = peewee.CharField(max_length=100)
    date_added = peewee.DateTimeField()
    release_year = peewee.IntegerField()
    rating = peewee.CharField(max_length=10)
    duration = peewee.CharField(max_length=10)
    listed_in = peewee.CharField(max_length=50)
    description = peewee.CharField(max_length=500)
    class Meta:
        database = database
        db_table = 'hulu_movies'

class Netflix(peewee.Model):
    show_id = peewee.PrimaryKeyField()
    type = peewee.CharField(max_length=50)
    title = peewee.CharField(max_length=100)
    director = peewee.CharField(max_length=50)
    cast = peewee.CharField(max_length=300)
    country = peewee.CharField(max_length=100)
    date_added = peewee.DateTimeField()
    release_year = peewee.IntegerField()
    rating = peewee.CharField(max_length=10)
    duration = peewee.CharField(max_length=10)
    listed_in = peewee.CharField(max_length=50)
    description = peewee.CharField(max_length=500)
    class Meta:
        database = database
        db_table = 'netflix_movies'

def upload():
    dict_tables = {
        'amazon':AmazonPrime,
        'disney':DisneyPlus,
        'hulu':Hulu,
        'netflix':Netflix
    }
    for key, value in zip(dict_tables.keys(),dict_tables.values()):        
        if value.table_exists():
            value.drop_table()
        value.create_table()
        
        with open(f'data/{key}.json') as file:
                # Convertimos todo el contenido a un listado de diccionario que representa cada usuario
                data = json.load(file)
        
        query = value.insert_many(data)
        query.execute()
        print(f'Carga de "{key}.json" completado Exitosamente!!')

if __name__ == '__main__':
    upload()
