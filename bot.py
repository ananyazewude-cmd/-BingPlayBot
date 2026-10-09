import os
import random
import asyncio
from gtts import gTTS
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiohttp import web

# 1. የቦት ቶክን እና የባለቤት መረጃዎች
BOT_TOKEN = "8706459996:AAErENBjKn9pm31C57w9xrcWBMYWUvNXU9Q"
OWNER_NAME = "Ananya Adefris"
TELEBIRR_NO = "0979152240"
CBE_BIRR_NO = "0979152240"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 2. ልክ እንደ ቤተሰብ ቢንጎ (Beteseb Bingo) የተሰራ ውብ የውስጥ ጨዋታ ገጽ (HTML)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Beteseb Bingo Interface</title>
    <script src="https://telegram.org"></script>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #1c1d30; color: white; margin: 0; padding: 10px; display: flex; flex-direction: column; align-items: center; }
        .stats-container { display: flex; justify-content: space-around; width: 100%; max-width: 450px; background-color: #2e1d62; padding: 8px 4px; border-radius: 6px; margin-bottom: 12px; font-size: 11px; font-weight: bold; text-align: center; }
        .stat-box { display: flex; flex-direction: column; gap: 2px; }
        .stat-val { color: #ffbe00; font-size: 13px; }
        .main-layout { display: flex; gap: 8px; width: 100%; max-width: 450px; }
        .left-board { display: grid; grid-template-columns: repeat(5, 1fr); gap: 3px; background-color: #272848; padding: 6px; border-radius: 8px; width: 45%; }
        .right-board { display: flex; flex-direction: column; width: 55%; gap: 10px; background-color: #232442; padding: 10px; border-radius: 8px; align-items: center; }
        .num-btn { background-color: #3d3e6a; color: #b3b5cb; border: none; font-size: 10px; font-weight: bold; padding: 5px 0; border-radius: 3px; text-align: center; }
        .num-btn.taken { background-color: #e67e22; color: white; }
        .called-ball-display { background-color: #ffbe00; color: #1c1d30; font-size: 24px; font-weight: bold; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.3); margin-bottom: 5px; }
        .switch-container { display: flex; align-items: center; justify-content: space-between; width: 90%; font-size: 12px; font-weight: bold; margin-bottom: 5px; }
        .bingo-letters { display: flex; gap: 3px; width: 100%; justify-content: center; margin-bottom: 4px; }
        .b-let { font-size: 14px; font-weight: bold; padding: 4px 10px; border-radius: 3px; background-color: #00a8ff; color: white; }
        .cartela-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 4px; width: 100%; }
        .cart-cell { background-color: white; color: #1c1d30; font-size: 14px; font-weight: bold; padding: 8px 0; border-radius: 4px; text-align: center; }
        .cart-cell.star { background-color: #2ecc71 !important; color: #ffbe00; font-size: 16px; }
        .cartela-tag { font-size: 10px; color: #ffbe00; margin-top: 4px; }
        .bottom-actions { display: flex; gap: 8px; width: 100%; max-width: 450px; margin-top: 12px; }
        .act-btn { flex: 1; border: none; padding: 10px 0; font-size: 13px; font-weight: bold; border-radius: 5px; color: white; cursor: pointer; }
        .act-btn.leave { background-color: #ff4757; }
        .act-btn.refresh { background-color: #e67e22; }
        .act-btn.main-auto { background-color: #57606f; background: linear-gradient(135deg, #e67e22, #f39c12); font-size: 14px; padding: 12px 0; border-radius: 6px; width: 100%; }
    </style>
</head>
<body>
    <div class="stats-container">
        <div class="stat-box"><div>Game ID</div><div class="stat-val">BX-9972</div></div>
        <div class="stat-box"><div>Players</div><div class="stat-val">335</div></div>
        <div class="stat-box"><div>Bet</div><div class="stat-val">10</div></div>
        <div class="stat-box"><div>Derash</div><div class="stat-val">2680</div></div>
        <div class="stat-box"><div>Called</div><div class="stat-val">0</div></div>
    </div>
    <div class="main-layout">
        <div class="left-board" id="leftBoard"></div>
        <div class="right-board">
            <div class="called-ball-display" id="ballDisplay">--</div>
            <div class="switch-container"><span>Automatic</span><span style="color:#2ecc71;">● ON</span></div>
            <div class="bingo-letters">
                <div class="b-let">B</div><div class="b-let">I</div><div class="b-let">N</div><div class="b-let">G</div><div class="b-let">O</div>
            </div>
            <div class="cartela-grid" id="cartelaMatrix"></div>
            <div class="cartela-tag">Cartela No: 131</div>
        </div>
    </div>
    <div class="bottom-actions">
        <button class="act-btn leave" onclick="tg.close()">Leave</button>
        <button class="act-btn refresh" onclick="location.reload()">Refresh</button>
    </div>
    <div style="width:100%; max-width:450px; margin-top:8px;">
        <button class="act-btn main-auto" onclick="startAutomaticDraw()">Automatic</button>
    </div>
    <script>
        const tg = window.Telegram.WebApp; tg.expand();
        const leftBoard = document.getElementById('leftBoard');
        const takenNumbers =;
        for (let row = 0; row < 15; row++) {
            for (let col = 0; col < 5; col++) {
                const num = col * 15 + (row + 1);
                const btn = document.createElement('div');
                btn.className = 'num-btn'; btn.innerText = num;
                if (takenNumbers.includes(num)) btn.classList.add('taken');
                leftBoard.appendChild(btn);
            }
        }
        const cartelaGrid = document.getElementById('cartelaMatrix');
        const myCartelaNumbers = [14, 24, 38, 49, 67, 6, 21, 40, 59, 61, 2, 20, '⭐', 48, 72, 9, 18, 45, 54, 73, 7, 29, 42, 58, 74];
        myCartelaNumbers.forEach((val) => {
            const cell = document.createElement('div'); cell.className = 'cart-cell'; cell.innerText = val;
            if (val === '⭐') cell.classList.add('star');
            cartelaGrid.appendChild(cell);
        });
        function startAutomaticDraw() {
            tg.sendData(JSON.stringify({action: "start_automatic", cartela: [14, 24, 38, 49, 67, 6, 21, 40, 59, 61, 2, 20, 48, 72, 9, 18, 45, 54, 73, 7, 29, 42, 58, 74]}));
            tg.showAlert("አውቶማቲክ ማጫወቻው ተነስቷል!");
        }
    </script>
</body>
</html>
"""

def generate_amharic_voice(text, filename="voice.mp3"):
    try:
        tts = gTTS(text=text, lang='am', slow=False)
        tts.save(filename)
        return filename
    except Exception:
        return None

# 3. የቤተሰብ ቢንጎ ማራኪ ሜኑ ቁልፎች (Inline Buttons)
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

# 4. የቁልፎች ተግባር ምላሽ ማስተናገጃ (Indentation የተስተካከለበት ቦታ)
@dp.callback_query()
async def button_click(query: types.CallbackQuery):
    data = query.data
    if data == "deposit":
        await query.message.answer(f"💰 ገንዘብ ለማስገባት፦\n\n▪️ ቴሌብር፦ {TELEBIRR_NO}\n▪️ ሲቢኢ ብር፦ {CBE_BIRR_NO}\n▪️ ስም፦ {OWNER_NAME}")
    elif data == "balance":
        await query.message.answer("💵 የአሁኑ ሂሳብዎ 200 ETB ነው።")
    else:
        await query.message.answer(f"ℹ️ ይህ {data} አገልግሎት በቅርቡ ይከፈታል!")

# 5. አውቶማቲክ ማጫወቻው ዳታ ሲልክ ዕጣ ማውጣት
@dp.message(lambda msg: msg.web_app_data)
async def web_app_data_handler(message: types.Message):
    import json
    data = json.loads(message.web_app_data.data)
    cartela_numbers = data.get("cartela", [])
    
    voice_text = "ቢንጎ ተጀምሯል! አውቶማቲክ ማጫወቻው ቁጥሮችን እየመረጠ ነው። መልካም ዕድል!"
    voice_file = generate_amharic_voice(voice_text)
    await message.answer("🗣 ጨዋታው ተጀምሯል! የአማርኛ ድምፅ መልዕክት እየተላከ ነው...")
    if voice_file and os.path.exists(voice_file):
        await message.answer_voice(voice=types.FSInputFile(voice_file))
        os.remove(voice_file)

    drawn_numbers = []
    for i in range(1, 6):
        await asyncio.sleep(4)
        lucky_pick = random.randint(1, 75)
        drawn_numbers.append(lucky_pick)
        
        prefix = 'B' if lucky_pick <= 15 else 'I' if lucky_pick <= 30 else 'N' if lucky_pick <= 45 else 'G' if lucky_pick <= 60 else 'O'
        ball_text = f"{prefix}-{lucky_pick}"
        
        await message.answer(f"🔮 ዙር {i} ዕጣ ወጣ! የወጣው ኳስ፦ 【 {ball_text} 】 ነው!")
        
        v_ball = generate_amharic_voice(f"የወጣው ቁጥር {lucky_pick}")
        if v_ball and os.path.exists(v_ball):
            await message.answer_voice(voice=types.FSInputFile(v_ball))
            os.remove(v_ball)

    matches = set(cartela_numbers).intersection(set(drawn_numbers))
    if len(matches) >= 1:
