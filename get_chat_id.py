import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()  # Load biến môi trường từ .env

# Lấy token từ biến môi trường hoặc .env
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

# Khởi tạo bot với token của Telegram
bot = Bot(token=bot_token)

# Hàm bất đồng bộ để lấy các cập nhật từ Telegram
async def get_chat_id():
    updates = await bot.get_updates()  # Sử dụng await để đợi phản hồi từ API
    for update in updates:
        print(f"Chat ID: {update.message.chat_id}")

# Chạy hàm bất đồng bộ với asyncio
if __name__ == "__main__":
    asyncio.run(get_chat_id())  # Chạy hàm bất đồng bộ get_chat_id
