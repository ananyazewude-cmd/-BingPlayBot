import os
import random
import asyncio
from gtts import gTTS
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# 1. አዲሱ የቦት ቶክን እና የባለቤት መረጃዎች
BOT_TOKEN = "8706459996:AAGldV22qcQZHOcUDs6ugOf9D_D3KafqyiY"
OWNER_NAME = "Ananya Adefris"
TELEBIRR_NO = "0979152240"
CBE_BIRR_NO = "0979152240"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# የጨዋታ መቆጣጠሪያ ዳታ
game_state = {
    "is_active": False,
    "selected_numbers": {},
    "pool": list(range(1, 97))
}

# የአማርኛ ድምፅ ማመንጫ ተግባር
def generate_amharic_voice(text, filename="voice.mp3"):
    try:
        tts = gTTS(text=text, lang='am', slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"የድምፅ ስህተት: {e}")
        return None

# የ /start ትዕዛዝ ሲላክ
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user = message.from_user
    welcome_text = (
        f"እንኳን ወደ ቢንጎ ኤክስ (BingoX) በደህና መጡ {user.first_name}!\n\n"
        f"💳 የሳፖርት እና ክፍያ መረጃዎች፦\n"
        f"▪️ ስም፦ {OWNER_NAME}\n"
        f"▪️ ቴሌብር፦ {TELEBIRR_NO}\n"
        f"▪️ ሲቢኢ ብር፦ {CBE_BIRR_NO}\n\n"
        f"ለመጫወት ከታች ያለውን '🎮 ጨዋታ ጀምር' የሚለውን ቁልፍ ይጫኑ።"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 ጨዋታ ጀምር", callback_data="start_game")],
        [InlineKeyboardButton(text="💵 ብር አስገባ (Deposit)", callback_data="deposit")]
    ])
    await message.answer(text=welcome_text, reply_markup=keyboard)

# የቁልፎች ምላሽ ማስተናገጃ
@dp.callback_query()
async def button_click(query: types.CallbackQuery):
    user_id = query.from_user.id

    if query.data == "start_game":
        if game_state["is_active"]:
            await query.message.answer("ጨዋታው ቀድሞውኑ ተጀምሯል! እባክዎ ዕጣው እስኪወጣ ይጠብቁ።")
            return
            
        game_state["is_active"] = True
        
        # ጨዋታ ሲጀመር በአማርኛ ድምፅ እንዲናገር ማድረግ
        voice_text = "ቢንጎ ተጀምሯል! አውቶማቲክ ማጫወቻው ቁጥሮችን እየመረጠ ነው። መልካም ዕድል!"
        voice_file = generate_amharic_voice(voice_text)
        
        await query.message.answer("🗣 ጨዋታው ተጀምሯል! የአማርኛ ድምፅ መልዕክት እየተላከ ነው...")
        
        if voice_file and os.path.exists(voice_file):
            voice_media = types.FSInputFile(voice_file)
            await query.message.answer_voice(voice=voice_media)
            os.remove(voice_file)

        # አውቶማቲክ ማጫወቻ (Auto Match)
        user_numbers = random.sample(game_state["pool"], 3)
        game_state["selected_numbers"][user_id] = user_numbers
        
        await query.message.answer(f"🎲 አውቶማቲክ ማጫወቻው የመረጣልዎት ቁጥሮች፦ {user_numbers}")
        
        # ከ3 ሰከንድ በኋላ አውቶማቲክ ዕጣ ማውጣት
        await asyncio.sleep(3)
        await run_lucky_draw(query.message)

    elif query.data == "deposit":
        deposit_text = (
            f"💰 ገንዘብ ለማስገባት ከታች ባሉት አካውንቶች ያስገቡና ማረጋገጫውን ለሳፖርት ይላኩ፦\n\n"
            f"▪️ ቴሌብር፦ {TELEBIRR_NO}\n"
            f"▪️ ሲቢኢ ብር፦ {CBE_BIRR_NO}\n"
            f"▪️ ስም፦ {OWNER_NAME}"
        )
        await query.message.answer(deposit_text)

# አውቶማቲክ የዕጣ ማውጫ ሲስተም
async def run_lucky_draw(message: types.Message):
    winning_number = random.randint(1, 96)
    await message.answer(f"🔮 የማሽኑ ዕጣ ወጥቷል! የአሸናፊው ቁጥር፦ 【 {winning_number} 】 ነው!")
    
    winners = []
    for user_id, numbers in game_state["selected_numbers"].items():
        if winning_number in numbers:
            winners.append(user_id)
            
    if winners:
        await message.answer("🎉 እንኳን ደስ አለዎት! አሸንፈዋል። ቴሌብርዎ ላይ ብር ገቢ ይደረጋል።")
        # አሸናፊ ሲኖር በአማርኛ ድምፅ መናገር
        v_file = generate_amharic_voice("እንኳን ደስ አለዎት አሸንፈዋል!")
        if v_file:
            voice_media = types.FSInputFile(v_file)
            await message.answer_voice(voice=voice_media)
            os.remove(v_file)
    else:
        await message.answer("😢 ለዚህ ዙር አልደረሶትም! ድጋሚ ይሞክሩ።")
        
    # ጨዋታውን ለቀጣዩ ዙር ማጽዳት
    game_state["is_active"] = False
    game_state["selected_numbers"] = {}

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
