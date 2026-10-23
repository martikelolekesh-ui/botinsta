import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
import yt_dlp
from aiohttp import web

TOKEN = "8815823364:AAEB3oEiH0-qLgPiJxWOK9MneJUXDO3lR90"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text.startswith("http"))
async def download_instagram(message: Message):
    url = message.text.strip()
    await message.answer("⏳ در حال دریافت ویدیو از اینستاگرام، لطفاً کمی صبر کنید...")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.mp4',
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        video_file = FSInputFile("downloaded_video.mp4")
        await message.answer_video(video_file, caption="✅ ویدیوی شما با موفقیت دانلود شد!")
        
    except Exception as e:
        await message.answer(f"❌ متأسفانه دانلود ویدیو با خطا مواجه شد:\n{str(e)}")

@dp.message()
async def start_handler(message: Message):
    await message.answer("سلام! 👋\nلینک پست یا ریلز اینستاگرام رو برام بفرست تا ویدیوش رو برات دانلود کنم.")

# وب‌سرور ساده برای پاسخ به درخواست‌های Render
async def handle(request):
    return web.Response(text="Bot is alive!")

async def run_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # همزمان هم وب‌سرور را روشن می‌کنیم هم ربات تلگرام را
    asyncio.create_task(run_web_server())
    print("ربات و وب‌سرور روشن شدند...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())