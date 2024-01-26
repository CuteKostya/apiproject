import requests
import datetime

import pymysql
from config import host, user, password, db_name


try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
    )
    print('true')

    try:
        with connection.cursor() as cursor:
            # Задаем координаты населенного пункта
            lat = 55.75396  # широта Москвы
            lon = 37.620393  # долгота Москвы

            # Задаем параметры запроса
            params = {
                'lat': lat,
                'lon': lon,
                'lang': 'ru_RU',  # язык ответа
                'limit': 7,  # срок прогноза в днях
                'hours': True,  # наличие почасового прогноза
                'extra': False  # подробный прогноз осадков
            }
            api_key = '0e154f3b-f244-4499-914a-afd124b6032a'

            # Задаем URL API
            url = 'https://api.weather.yandex.ru/v2/informers'

            response = requests.get(url, params=params, headers={'X-Yandex-API-Key': api_key})

            print(response.json())

            data = response.json()

            insert_query = ("INSERT INTO `weather` (obs_time, temp, feels_like, icon, `condition`, wind_speed, wind_dir, pressure_mm, pressure_pa, daytime, polar, season, wind_gust)"
                            " VALUES ( data[`fact`]['obs_time'], data['fact']['temp'], data['fact']['feels_like'], data['fact']['icon'], data['fact']['condition'], data['fact']['wind_speed'], data['fact']['wind_dir'], data['fact']['pressure_mm'], data['fact']['pressure_pa'], data['fact']['daytime'], data['fact']['polar'], data['fact']['season'], data['fact']['wind_gust'])")
            cursor.execute(insert_query)
            connection.commit()
    finally:
        connection.close()
except Exception as ex:
    print('false')
    print(ex)



sql = "INSERT INTO likes ( user_id, post_id ) VALUES ( %s, %s )"
val = [(4, 5), (3, 4)]

cursor = connection.cursor()
cursor.executemany(sql, val)
connection.commit()





















# Задаем координаты населенного пункта
lat = 55.75396  # широта Москвы
lon = 37.620393  # долгота Москвы

# Задаем параметры запроса
params = {
    'lat': lat,
    'lon': lon,
    'lang': 'ru_RU',  # язык ответа
    'limit': 7,  # срок прогноза в днях
    'hours': True,  # наличие почасового прогноза
    'extra': False  # подробный прогноз осадков
}

# Задаем значение ключа API
api_key = '0e154f3b-f244-4499-914a-afd124b6032a'

# Задаем URL API
url = 'https://api.weather.yandex.ru/v2/informers'

# Делаем запрос к API
response = requests.get(url, params=params, headers={'X-Yandex-API-Key': api_key})

print(type(response.json()))
# Проверяем статус ответа
if response.status_code == 200:
    # Преобразуем ответ в JSON формат
    data = response.json()

    # Выводим данные о текущей погоде
    print(f'Температура воздуха: {data["fact"]["temp"]} °C')
    print(f'Ощущается как: {data["fact"]["feels_like"]} °C')
    print(f'Скорость ветра: {data["fact"]["wind_speed"]} м/с')
    print(f'Давление: {data["fact"]["pressure_mm"]} мм рт. ст.')
    print(f'Влажность: {data["fact"]["humidity"]} %')
    print(f'Погодное описание: {data["fact"]["condition"]}')
else:
    # Выводим код ошибки
    print(f'Ошибка: {response.status_code}')
