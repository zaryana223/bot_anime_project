# Импорт токена бота из файла config.py
from config import TOKEN

# Импорт нужных функций для взаим-я с пользователем 
from handlers import greet_user, send_plot, show_techs, show_tech_info
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
import logging

# Настройка логирования, чтобы ловить всякие баги 
logging.basicConfig(
    filename='bot.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    )

# Основная функция, запускающая бота
def main():
    bot = Updater(TOKEN)
    dp = bot.dispatcher

    dp.add_handler(CommandHandler('start', greet_user))

    # Фильтр сообщений с помощью регулярного выражения
    # r'^([\d]{1,3})$' означает, что будет приниматься только текст, состоящий из 1-3 цифр
    dp.add_handler(MessageHandler(Filters.regex(r'^([\d]{1,3})$'), show_techs))

    dp.add_handler(MessageHandler(Filters.regex('ТОП-10'), send_plot))
    dp.add_handler(CallbackQueryHandler(show_tech_info))
    
    # Бот проверяет есть ли какие-то обновления + ходит бесконечным циклом 
    # (привет! для меня есть работа) иииииии так бесконечно
    bot.start_polling()
    bot.idle()

# Проверка, является ли данный файл главным файлом программы
if __name__ == '__main__':
    main()
