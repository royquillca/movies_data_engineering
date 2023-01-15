from collections import Counter
from src.lib.managedb import Movies




#-------------------------------------------------------------------------#
# Consultas de peewee
# Máxima duración según tipo de film (película/serie), por plataforma y por año:
# El request debe ser: get_max_duration(año, plataforma, [min o season])
#-------------------------------------------------------------------------#

def get_max_duration(year, platform, min_or_season):

    def type_min_season(min_or_season):
        if (min_or_season.lower() == 'min') or (min_or_season.lower() == 'minutes'):
            type = 'Movie'
        elif (min_or_season.lower() == 'season') or (min_or_season.lower() == 'seasons'):
            type = 'Tv show'
        return type

    if type_min_season(min_or_season) == 'Movie':

        max_duration = Movies.select(Movies.duration).where(
            (Movies.type == 'Movie') & (Movies.release_year == year) & (
                Movies.platform == platform)
        ).order_by(
            Movies.duration.desc()
        ).limit(1).get()
        # print(f'La máxima duración de la lista de {type_min_season(min_or_season)} en la plataforma {platform} lanzado en el año {year} es de {max_duration.duration}')
        return {
            'type': type_min_season(min_or_season),
            'platform': platform, 
            'year': year, 
            'type_time': min_or_season,
            'max_duration': max_duration.duration
            }

    elif type_min_season(min_or_season) == 'Tv show':
        max_duration = Movies.select(Movies.duration).where(
            (Movies.type == 'Tv Show') & (Movies.release_year == year) & (
                Movies.platform == platform)
        ).order_by(Movies.duration.desc()).limit(1).get()

        # print(f'La máxima duración de la lista de {type_min_season(min_or_season)} en la plataforma {platform} lanzado en el año {year} es de {max_duration.duration}')
        return {
            'type': type_min_season(min_or_season), 
            'platform': platform, 
            'year': year, 
            'type_time': min_or_season,
            'max_duration': max_duration.duration
            }
    # return {'type':type_min_season(min_or_season),'platform':platform, 'year':year, 'max_duration':max_duration.duration}

print(get_max_duration(2010, 'hulu', 'season'))


#-----------------------------------------------------------#
# Cantidad de películas y series (separado) por plataforma.
# El request debe ser: get_count_plataform(plataforma)
#-----------------------------------------------------------#

def get_count_platform(platform):
    def get_count_by_type(type):
        total_films = Movies.select().where((Movies.platform == platform)
                                            & (Movies.type == type)).count()
        return total_films
    # print(f'La plataforma {platform} tiene:\n* Cantidad de peliculas: {get_count_by_type("Movie")}\n* Cantidad de series: {get_count_by_type("Tv show")}')
    return {
        'platform': platform,
        'total_movies': get_count_by_type('Movie'),
        'total_series': get_count_by_type('Tv Show'),
    }
# get_count_platform('hulu')
# print(get_count_platform('hulu'))


#----------------------------------------------------------------------------------------#
# Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
# El request debe ser: get_listedin('genero')
#----------------------------------------------------------------------------------------#

def get_listedin(genre):
    def get_count_by_platform(platform):
        amount = Movies.select().where((Movies.platform == platform) &
                                       (Movies.listed_in ** f'%{genre}%')).count()
        return amount
    # ['amazon_prime', 'disney_plus', 'hulu', 'netflix']
    # print(f'El género {genre} tiene las siguientes cantidades de frecuencias de acuerdo a la plataforma:\n* Amazon Prime: {get_count_by_platform("amazon_prime")}\n* Disney Plus: {get_count_by_platform("disney_plus")}\n* Hulu: {get_count_by_platform("hulu")}\n* Netflix: {get_count_by_platform("netflix")}')

    return {
        'genre': genre,
        'amazon_prime_duplicates': get_count_by_platform('amazon_prime'),
        'disney_plus_duplicates': get_count_by_platform('disney_plus'),
        'hulu_duplicates': get_count_by_platform('hulu'),
        'netflix_duplicates': get_count_by_platform('netflix')
    }

# get_listedin('comedy')
# print(get_listedin('comedy'))

#------------------------------------------------------#
# Actor que más se repite según plataforma y año.
# El request debe ser: get_actor(plataforma, año)
#------------------------------------------------------#


def get_actor(platform, year):
    # Obtener todos los actores
    actors = []
    for movie in Movies.select().where((Movies.platform == platform) & (Movies.release_year == year)):
        actors += movie.cast.split(',')

    # Contar la cantidad de veces qe aparece cada actor
    actor_count = Counter(actors)

    # Obtener el actor con el mayor cantidad de repeticiones
    most_common_actor = actor_count.most_common(5)
    
    return {
        'most_common_actors': most_common_actor
    }
    
    # print(f'El top {len(most_common_actor)} de los actores con mayor cantidad participación en las películas o series de la plataforma {platform} en el año {year} son:')
    # counter = 0
    
    # for actor in most_common_actor:
    #     counter += 1
    #     print(f'{counter}°: {actor[0]} tuvo {actor[1]} partipaciones.')

# print(get_actor('netflix',2000))
