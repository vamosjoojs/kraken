import telegram
from app.config.config import config


class TelegramIntegration:
    @staticmethod
    def send_message(message: str):
        bot = telegram.Bot(config.TELEGRAM_TOKEN)
        bot.send_message(text=message, chat_id=-766378975)
