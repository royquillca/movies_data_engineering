from fastapi import FastAPI, Response

from src.router.routes import get_actor, get_listedin, get_count_platform, get_max_duration
from src.lib.managedb import database as connection
# from src.router.routes import get_actor, get_listedin, get_count_platform, get_max_duration

app = FastAPI(
    title='Lista de Películas',
    description='Proyecto que disponibiliza la lista de películas de diferentes fuentes de diversos servicios de suscripción de streaming de vídeo: Amazon Prime, Netflix, Hulu, Disney Plus.',
    version='0.0.1'
)

css_style = """<style> 
    body { 
        font-family: Arial, sans-serif;
        font-size: 16px;
        color: #FF5733;
        background-color: #FFFF;
    }
    p {
        padding-top:0px;
        margin-bottom: 2px;
    }
    ol {
        margin-block-start: 1px;
        padding-inline-start: 18px;
    }
    ul {
        margin-block-start: 1px;
        padding-inline-start: 18px;
    }
    h2 {
        padding-top: 50px;
        color: #08D995;
    }
</style>"""


# Inicializando el servidor de FastAPI
@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
        print('Inicializando el servidor de FastAPI')

# Probando el servidor en root "/"
@app.get('/')
async def root():
    return Response(content=css_style + '<h2 align="center">Respuesta de inicialización exitosa del servidor de FastAPI</h2>', media_type='text/html')

#-------------------------------------#
#------------- Consulta 1-------------#
#-------------------------------------#

@app.get('/get_max_duration/{year}/{platform}/{type_time}')
async def pregunta_1(year: int, platform: str,type_time: str):
    json_response = get_max_duration(year, platform, type_time)
    # return json_response
    # http://localhost:8000/get_max_duration/2010/hulu/min    
    return Response(content=css_style + f'<p>La <b>máxima duración</b> de la lista de <b>{json_response["type"]}</b> en la plataforma <b>{json_response["platform"]}</b> lanzado en el año <b>{json_response["year"]}</b> es de <b>{json_response["max_duration"]} {json_response["type_time"]}.</b></p>', media_type='text/html')


#-------------------------------------#
#------------- Consulta 2-------------#
#-------------------------------------#

@app.get('/get_count_platform/{platform}')
async def pregunta_2(platform:str):
    json_response = get_count_platform(platform)
    # return json_response
    # http://localhost:8000/get_count_platform/hulu
    
    # return Response(content=css_style + f'<p>La plataforma {json_response["platform"]} tiene:</p>\n <ol> Cantidad de peliculas: {json_response["total_movies"]}</ol>\n <ol> Cantidad de series: {json_response["total_series"]}</ol>', media_type='text/html')
    
    return Response(content=css_style + f'<p>La plataforma <b>{json_response["platform"]}</b> tiene:</p> <ol><li>Cantidad de peliculas: <b>{json_response["total_movies"]}</b></li><li>Cantidad de series: <b>{json_response["total_series"]}</b></li></ol>', media_type='text/html')

#-------------------------------------#
#------------- Consulta 3-------------#
#-------------------------------------#

@app.get('/get_listedin/{genre}')
async def pregunta_3(genre: str):
    json_response = get_listedin(genre)
    # return json_response
    # http://localhost:8000/get_listedin/comedy
    return Response(content=css_style + f'<p>El género {json_response["genre"]} tiene las siguientes cantidades de frecuencias de acuerdo a la plataforma:</p> <ul><li>Amazon Prime: <b>{json_response["amazon_prime_duplicates"]}</b> registros de películas/series.</li><li>Disney Plus: <b>{json_response["disney_plus_duplicates"]}</b> registros de películas/series.</li><li>Hulu: <b>{json_response["hulu_duplicates"]}</b> registros de películas/series.</li><li>Netflix: <b>{json_response["netflix_duplicates"]}</b> registros de películas/series.</li></ul>', media_type='text/html')


#-------------------------------------#
#------------- Consulta 4-------------#
#-------------------------------------#

@app.get('/get_actor/{platform}/{year}')
async def pregunta_4(platform:str, year:int):
    json_response = get_actor(platform, year)
    # return json_response
    # http://localhost:8000/get_actor/netflix/2000
    actors_str =css_style + f'<p>El <b>top 5</b> de los <b>actores con mayor cantidad participación</b> en las películas o series de la plataforma <b>{platform}</b> en el año <b>{year}</b> son:</p>'
    counter = 0
    for actor in json_response['most_common_actors']:
        counter += 1
        actors_str += css_style + f'{counter}°: <b>{actor[0]}</b> tuvo <b>{actor[1]}</b> partipaciones.</br>'
    return Response(content= actors_str, media_type='text/html')

# Finalizando el servidor de FastAPI
@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        print('Finalizando el servidor de FastAPI')