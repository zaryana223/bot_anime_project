# Импорт необходимых модулей и функций
from db import db_session
from models import Technique, User
from utils import get_kb, get_techs_kb
from io import BytesIO
import matplotlib.pyplot as plt
plt.switch_backend('Agg')  # Установка фонового режима для matplotlib
from sqlalchemy import desc
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
import logging

# Настройка логирования 
logging.basicConfig(filename='bot.log', level=logging.INFO)

# Добавление нового пользователя 
def add_user(message):
    telegram_id = message.chat.id
    check_user = User.query.filter_by(telegram_id=telegram_id).first()
    if not check_user:
        username = message.chat.username
        new_user = User(
            telegram_id=telegram_id,
            username=username,
        )
        db_session.add(new_user)
        db_session.commit()

# Функция для приветствия пользователя и запроса номера эпизода
def greet_user(update: Update, context: CallbackContext):
    name = update.message.chat.username
    update.message.reply_text(
        f'''Привет, {name.capitalize()}!
Вбей номер эпизода, и я покажу тебе список техник''',
        reply_markup=get_kb(),
        )
    add_user(update.message)

# Функция для отправки графика с топ-10 техник
def send_plot(update: Update, context: CallbackContext):

    # Получение данных из БД, берем 10 техник с наибольшим значением каунтера и сортируем по убыванию
    all_techs = Technique.query.order_by(desc(Technique.counter)).all()[:10]
    x = []
    y = []
    for tech in all_techs:
        x.append(tech.name)
        y.append(tech.counter)

    # Создания графика
    plt.figure(dpi=160)
    plt.barh(x, y, color='lightblue')
    plt.title('ТОП-10 техник по кол-ву запросов')
    plt.grid(True)
    plt.xlabel('Кол-во запросов')
    plt.ylabel('Техники')

    # Создание байтового потока для отправки изображения
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)

    context.bot.send_photo(
        chat_id=update.message.chat.id,
        photo=buffer
    )
    
    plt.close()
    
    update.message.reply_text('Вбей номер эпизода, и я покажу тебе список техник')


# Функция для отображения списка техник для заданного эпизода
def show_techs(update: Update, context: CallbackContext):
    try:
        text = update.message.text        
        check_episode = Technique.query.filter_by(episode=text).all()
        if check_episode:
            update.message.reply_text(
                'Выбери интересующую технику:',
                reply_markup=get_techs_kb(check_episode),
            )
        else:
            update.message.reply_text('Нет информации о данном эпизоде')            
    except Exception as e:
        logging.error(f"Ошибка в функции show_techs: {e}")


def show_tech_info(update: Update, context: CallbackContext):
    update.callback_query.answer('Ожидайте...')

    # Получить данные о выбранной технике из callback_data
    tech = update.callback_query.data
    tech = Technique.query.get(int(tech)) # Здесь (int(tech)), потому что callback_data = id (технике)
    if tech:
        tech.counter += 1
        db_session.commit()
        text = f'Техника: {tech.name}\nСтихия: {tech.element}\nТип: {tech.type_tech}\nРанг: {tech.rank}'
        context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text=text,
            reply_markup=get_kb(),
        )     
        context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text='Вбей номер эпизода или выбери технику, о которой хочешь получить информацию',
        )   
    else:           
        # Если информация о технике не найдена, отправить следующее сообщение   
        context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text='Выберите одну из техник!',
        )
