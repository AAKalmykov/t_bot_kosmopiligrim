import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Применяем nest_asyncio для корректной работы asyncio в Colab
# (nest_asyncio removed: not needed on a server; it breaks httpx on Python 3.14)
# nest_asyncio.apply()

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
    logger.info("запуск Бота")
    """Запуск бота."""
    # close_loop=False решает проблему 'Cannot close a running event loop' в Colab
    application = Application.builder().token(TOKEN).build()
    logger.info("запуск Майн ")
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)

if __name__ == "__main__":
    main()
