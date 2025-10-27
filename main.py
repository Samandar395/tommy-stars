# majburiy_kanal_bot.py
# aiogram (v2) misoli — Python 3.8+
# o'rnatish: pip install aiogram

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import os

logging.basicConfig(level=logging.INFO)

# --- SOZLAMALAR ---
BOT_TOKEN = "7379852050:AAE42Nr8sRd1jeKUVWoPr-cnQlia0U4Al-k"   # BotFather token
CHANNEL_USERNAME = "@kotta_bolacha"                  # majburiy kanal username (masalan @mychannel)
# -------------------

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def join_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text="📣 Kanalga oʻtish", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"))
    kb.add(InlineKeyboardButton(text="✅ Men a'zo bo'ldim", callback_data="check_sub"))
    return kb

async def is_subscribed(user_id: int) -> bool:
    """
    Foydalanuvchi kanalga a'zo yoki admin/creator ekanligini tekshiradi.
    Agar get_chat_member exception qaytarsa (masalan kanal noma'lum yoki bot admin emas) -> False qaytaradi.
    """
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        # status: "creator", "administrator", "member", "restricted", "left", "kicked"
        if member.status in ("creator", "administrator", "member", "restricted"):
            return True
        return False
    except Exception as e:
        # logging uchun (masalan: Bot kanalga admin qilinmagan bo'lsa yoki kanal xususiy bo'lsa)
        logging.exception("get_chat_member xatosi: %s", e)
        return False

@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    ok = await is_subscribed(user_id)
    if ok:
        await message.reply("🎉 Xush kelibsiz! Siz kanalga a'zo bo'lgansiz — botdan foydalanishingiz mumkin.")
        # Bu yerga bot menyusi yoki boshqa funksiyalarni qo'shing
    else:
        text = (
            "⛔ Botdan foydalanishdan oldin quyidagi kanalga a'zo bo'lishingiz shart:\n"
            f"{CHANNEL_USERNAME}\n\n"
            "Iltimos kanalga obuna bo'ling, keyin «Men a'zo bo'ldim» tugmasini bosing."
        )
        await message.reply(text, reply_markup=join_keyboard())

@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def process_check_sub(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)  # tez feedback
    ok = await is_subscribed(user_id)
    if ok:
        await bot.send_message(user_id, "✅ Rahmat! Siz kanalga a'zo ekansiz. Endi botdan foydalanishingiz mumkin.")
        # Kerak bo'lsa davomiy menyuni shu yerga qo'shing
    else:
        await bot.send_message(
            user_id,
            "⚠️ Biz hali ham sizni kanal a'zosida deb topa olmadik. Iltimos kanalga obuna bo'lganingizni tekshiring va qayta urinib ko'ring.",
            reply_markup=join_keyboard()
        )

if name == "main":
    print("Bot ishga tushmoqda...")
    executor.start_polling(dp, skip_updates=True)
