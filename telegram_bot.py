import telegram
import os
from dotenv import load_dotenv
import asyncio
from queue import Queue
from threading import Thread

# Tải biến môi trường từ file .env
load_dotenv()

# Lấy token và chat ID từ biến môi trường
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

# Khởi tạo bot với token từ file .env
bot = telegram.Bot(token=bot_token)

# Hàng đợi tin nhắn
message_queue = Queue()

# Hàm bất đồng bộ để gửi tin nhắn đến một chat ID
async def send_telegram_message_async(message):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Lỗi khi gửi tin nhắn Telegram: {str(e)}")

# Hàm lấy tin nhắn từ hàng đợi và gửi
async def process_queue():
    while True:
        message = message_queue.get()  # Lấy tin nhắn từ hàng đợi
        if message is None:
            break  # Kết thúc nếu có yêu cầu dừng
        await send_telegram_message_async(message)
        message_queue.task_done()

# Hàm để bắt đầu vòng lặp sự kiện và xử lý hàng đợi
def start_asyncio_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_queue())

# Khởi động luồng xử lý tin nhắn Telegram
def start_telegram_thread():
    thread = Thread(target=start_asyncio_loop)
    thread.start()

# Hàm đồng bộ để đưa tin nhắn vào hàng đợi
def send_message_sync(message):
    message_queue.put(message)
