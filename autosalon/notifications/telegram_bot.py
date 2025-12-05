# notifications/telegram_bot.py
import asyncio
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters


class NotificationBot:
    def __init__(self, token):
        self.token = token
        self.bot = Bot(token=token)
        self.application = Application.builder().token(token).build()

    async def send_notification(self, chat_id, message):
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='HTML'
            )
            return True
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("subscribe", self.subscribe))

    async def start(self, update, context):
        await update.message.reply_text("Добро пожаловать в автосалон!")

    async def subscribe(self, update, context):
        # Регистрация пользователя для получения уведомлений
        chat_id = update.effective_chat.id
        # Сохраняем в базу данных
        await update.message.reply_text("Вы подписались на уведомления!")