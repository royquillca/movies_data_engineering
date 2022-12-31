import pandas as pd
from datetime import datetime
import numpy as np
import re


# Lectura de datasets
amazon_titles = pd.read_csv('./Datasets/amazon_prime_titles.csv')
disney_titles = pd.read_csv('./Datasets/disney_plus_titles.csv')
hulu_titles = pd.read_csv('./Datasets/hulu_titles.csv')
netflix_titles = pd.read_json('./Datasets/netflix_titles.json')


def drop_duplicates(df):
    df = df.drop('show_id', axis=1)
    
    if df.duplicated(df.columns).sum() > 0:
        print(f'Hay duplicados:\n{df[df.duplicated(df.columns)]}')
        print('Eliminando...')
        df.drop_duplicates()
    else:
        print('No hay duplicados!')
    return df

def solve_nan_vals(df):
    
    df['cast'] = df['cast'].replace(np.nan , 'Unavailable')
    df['director'] = df['director'].replace(np.nan , 'Unavailable')
    
    rating_mode = df['rating'].mode().values[0]
    df['rating'] = df['rating'].fillna(rating_mode)
    
    date_added_mode = df["release_year"].mode().values[0]
    df["date_added"] = df["date_added"].fillna(f'January 01, {date_added_mode}')
    
    df['country'] = df['country'].replace(np.nan, 'Unavailable')
    
    return df

def change_to_datetime(df):
    months = {'January':1 , 'February':2 , 'March':3 , 'April':4 , 'May':5 , 'June':6 , 'July':7 , 'August':8 , 
            'September':9 , 'October':10 , 'November':11 , 'December':12}    
    date_list = []
    for i in df["date_added"]:
        str1= re.findall('([a-zA-Z]+)\s[0-9]+\,\s[0-9]+' , i)
        str2= re.findall('[a-zA-Z]+\s([0-9]+)\,\s[0-9]+' , i)
        str3= re.findall('[a-zA-Z]+\s[0-9]+\,\s([0-9]+)' , i)
        dates = '{}-{}-{}'.format(str2[0] , months[str1[0]] , str3[0])
        date_list.append(dates)
    
    df['date_added'] = date_list
    df['date_added'] = pd.to_datetime(df['date_added'], format='%d-%m-%Y')
    
    return df

def solve_country_nan_vals(df):
    for i , j in zip(df["country"].values , df.index):
        if i == np.nan:
            if (('Anime' in df.loc[j,'listed_in']) or ('anime' in df.loc[j,'listed_in'])):
                print(j)
                df.loc[j,'country'] ='Japan'
            elif (('Western' in df.loc[j,'listed_in']) or ('western' in df.loc[j,'listed_in'])):
                print(j)
                df.loc[j,'country'] ='United States'
            else:
                continue
        else:
            continue
    return df

def cleaning(df, file_name):
    # Elimnar duplicados
    amazon_df = drop_duplicates(df)
    # Resolver los valores nulos (NAN)
    amazon_df = solve_nan_vals(amazon_df)
    # Cambiar el tipo de dato a datetime
    amazon_df = change_to_datetime(amazon_df)
    # Resolver valores nulos de la columna Country
    amazon_df = solve_country_nan_vals(amazon_df)
    

    # # Exportar a JSON: convierte el DataFrame a JSON con orientación 'records' (lista de diccionarios)
    json_data = amazon_df.to_json(orient='records')
    # Guarda el JSON en un archivo
    with open(f'./data/{file_name}', 'w') as f:
        f.write(json_data)

def upload_rows():
    dict_tables = {
        'amazon':amazon_titles,
        'disney':disney_titles,
        'hulu':hulu_titles,
        'netflix':disney_titles
    }
    for key, value in zip(dict_tables.keys(), dict_tables.values()):
        cleaning(value, f'{key}.json')
        print(f'Limpieza de "amazon.json" existosamente!!\n> {value.shape[0]} regitros cargados')

if __name__ == '__main__':
    upload_rows()