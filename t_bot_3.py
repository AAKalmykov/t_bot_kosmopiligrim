import logging
import telebot
import os

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Приветствие при старте."""
    user = message.from_user
    logger.info("Команда /start вызвана пользователем: %s (ID: %s)", user.full_name, user.id)
    
    welcome_text = f"Привет, {user.first_name}! Я бот-эхо. Напиши мне что-нибудь, и я повторю."
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Эхо-ответ на любое текстовое сообщение."""
    user = message.from_user
    text = message.text
    logger.info("Пользователь %s (ID: %s) написал: %s", user.full_name, user.id, text)
    
    bot.reply_to(message, text)

if __name__ == "__main__":
    print("Бот успешно запущен (без asyncio)...")
    # Запуск бесконечного цикла опроса обновлений
    bot.infinity_polling()
