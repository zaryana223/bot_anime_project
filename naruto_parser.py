# Импорт необходимых библиотек и функций
from bs4 import BeautifulSoup
from db import db_session
from models import Technique
import requests

# библиотека для создания прогресс-баров, во время парсинга виден его прогресс
from tqdm import tqdm 

# Функция для получения HTML-кода страницы с сайта о техниках Наруто
def get_html(url):
    # Имитируем поведение браузера, так как на сайте стоит защита от парсинга
    headers = {
        'Accept': '*/*', 'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1; rv:57.0.2) Gecko/20100101 Firefox/57.0.2',
        'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1',
        }
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return False

# Функция для парсинга характеристик техник (ищем стихию, тип, ранг)
def parse_tech_details(url):
    html = get_html(url)
    if html:
        result = {}
        soup = BeautifulSoup(html, 'html.parser')
        chakras = soup.find_all('div', class_='thisischakras clear')

        # Задаем список ключей для информации о технике
        # Итерируемся по индексам и ключам одновременно
        keys = ['element', 'type_tech', 'rank']
        for i, key in enumerate(keys):
            try:
                result[key] = chakras[i].find('ul').text.strip()
            except IndexError:
                # Так сделано, потому что, к примеру, у некоторых техник нет ранга
                result[key] = None 

                
        return result
    return False

# Функция для парсинга эпизодов
def parse_season(episodes):
    result = {}
    episodes = episodes.find_all('div', class_='series_item')
    for e in tqdm(episodes):
        episode = e.find('span').text.split()[0]
        result.setdefault(episode, {})
        techs = e.find('ul', class_='s_t_list').find_all('li')

        # Мы делаем длинну тегов 'а' = 2, потому что на сайте это может выглядит следующем образом:
        # 1 серия [значок][значок]Превращение, а мы берем только такие [значок]Превращение
        techs = filter(lambda t: len(t.find_all('a')) == 2, techs)         
        for t in techs:
            # Поиск второй ссылки в блоке 'a' и извлечение URL и текста
            t = t.find_all('a')[1]
            url = t['href']
            name = t.text
            result[episode][name] = {}
            result[episode][name]['url'] = url
            details = parse_tech_details(url)
            # Если детали успешно спарсены, добавляем их в словарь с информацией о технике
            if details:
                result[episode][name] |= details
    return result

# Функция для парсинга всех сезонов 
def parse_tech():
    url = 'https://jut.su/by-episodes/'
    html = get_html(url)
    if html:
        result = {}
        soup = BeautifulSoup(html, 'html.parser')
        first_season = soup.find('div', class_='series_lists')
        result = parse_season(first_season)
        save_data(result)

# Функция для сохранения данных о техниках в базу данных
def save_data(data):
    print('Начинаю сохранять...')
    for episode, techs in tqdm(data.items()):
        for tech, info in techs.items():
            new_tech = Technique(
                name=tech,
                link=info['url'],
                episode=episode,
                element=info['element'],
                type_tech=info['type_tech'],
                rank=info['rank']
            )
            db_session.add(new_tech)
            db_session.commit()
    print('готово!')


if __name__ == '__main__':
    print(parse_tech())
