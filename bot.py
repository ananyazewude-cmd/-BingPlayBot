import os
import random
import asyncio
from gtts import gTTS
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiohttp import web

BOT_TOKEN = "8706459996:AAErENBjKn9pm31C57w9xrcWBMYWUvNXU9Q"
OWNER_NAME = "Ananya Adefris"
TELEBIRR_NO = "0979152240"
CBE_BIRR_NO = "0979152240"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def generate_amharic_voice(text, filename="voice.mp3"):
    try:
        tts = gTTS(text=text, lang='am', slow=False)
        tts.save(filename)
        return filename
    except Exception:
        return None

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    server_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', '://onrender.com')}/webapp"
    welcome_text = (
        f"👋 Welcome to Beteseb Bingo! Choose an Option below.\n\n"
        f"👤 ስም፦ {OWNER_NAME}\n"
        f"💳 ቴሌብር፦ {TELEBIRR_NO}\n"
        f"🏦 CBE ብር፦ {CBE_BIRR_NO}"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Play 🎰", web_app=WebAppInfo(url=server_url)), InlineKeyboardButton(text="Register 📝", callback_data="register")],
        [InlineKeyboardButton(text="Check Balance 💵", callback_data="balance"), InlineKeyboardButton(text="Deposit 💰", callback_data="deposit")],
        [InlineKeyboardButton(text="Contact Support ☎️", callback_data="support"), InlineKeyboardButton(text="Instruction 📖", callback_data="instruction")],
        [InlineKeyboardButton(text="Transfer 🎁", callback_data="transfer"), InlineKeyboardButton(text="Withdraw 🤑", callback_data="withdraw")],
        [InlineKeyboardButton(text="Invite 🔗", callback_data="invite"), InlineKeyboardButton(text="Convert Bonus 💸", callback_data="bonus")]
    ])
    await message.answer(text=welcome_text, reply_markup=keyboard)

@dp.callback_query()
async def button_click(query: types.CallbackQuery):
    data = query.data
    if data == "deposit":
        await query.message.answer(f"💰 ገንዘብ ለማስገባት፦\n\n▪️ ቴሌብር፦ {TELEBIRR_NO}\n▪️ ሲቢኢ ብር፦ {CBE_BIRR_NO}\n▪️ ስም፦ {OWNER_NAME}")
    elif data == "balance":
        await query.message.answer("💵 የአሁኑ ሂሳብዎ 200 ETB ነው።")
    else:
        await query.message.answer(f"ℹ️ ይህ {data} አገልግሎት በቅርቡ ይከፈታል!")

@dp.message(lambda msg: msg.web_app_data)
async def web_app_data_handler(message: types.Message):
    voice_text = "ቢንጎ ተጀምሯል! አውቶማቲክ ማጫወቻው ቁጥሮችን እየመረጠ ነው። መልካም ዕድል!"
    voice_file = generate_amharic_voice(voice_text)
    await message.answer("🗣 ጨዋታው ተጀምሯል! የአማርኛ ድምፅ መልዕክት እየተላከ ነው...")
    if voice_file and os.path.exists(voice_file):
        await message.answer_voice(voice=types.FSInputFile(voice_file))
        os.remove(voice_file)
    await asyncio.sleep(2)
    await message.answer("🎉 ጨዋታው ተጠናቋል! አሸናፊዎቹ በዌብ አፑ ላይ ተገልጠዋል።")

# የቢንጎ መጫወቻ ገጽን ከውጭ የድረ-ገጽ ፋይል ላይ በቀጥታ የማንበቢያ ንፁህ ዘዴ
async def handle_webapp(request):
    # ሰርቨሩ የቢንጎውን ገጽ ከ index.html ላይ ያለምንም የኮድ ግጭት ያነባል
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return web.Response(text=content, content_type='text/html')
    except Exception:
        return web.Response(text="<h2>Error loading game interface. Make sure index.html exists on GitHub.</h2>", content_type='text/html')

async def handle_home(request): 
    return web.Response(text="Bot is running smoothly!")

async def start_bot():
    asyncio.create_task(dp.start_polling(bot))
    app = web.Application()
    app.router.add_get('/', handle_home)
    app.router.add_get('/webapp', handle_webapp)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080))).start()
    while True: 
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(start_bot())
