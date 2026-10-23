import os
import logging
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования для вывода в консоль
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Применяем nest_asyncio для корректной работы asyncio в Colab
nest_asyncio.apply()

# Токен вашего бота
TOKEN = os.environ.get('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение при команде /start и записывает это в лог."""
    user = update.effective_user
    logger.info("Команда /start вызвана пользователем: %s (ID: %s)", user.full_name, user.id)
    
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я бот-эхо. Напиши мне что-нибудь, и я повторю."
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Повторяет текстовые сообщения пользователя и логирует каждую полученную строку."""
    user = update.effective_user
    text = update.message.text
    logger.info("Пользователь %s (ID: %s) написал: %s", user.full_name, user.id, text)
    
    await update.message.reply_text(text)

def main() -> None:
    """Запуск бота."""
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    # Вы можете раскомментировать main() и запустить ячейку для старта бота
    main()
    pass
