import asyncio
import os
import secrets
import asyncpg
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
pool: asyncpg.Pool | None = None

# ── Keyboards ────────────────────────────────────────────────────────────────
CONTACT_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Kontaktingizni yuboring", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

RENEW_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔄 Renew / Yangilash")]],
    resize_keyboard=True,
)

# ── /start ───────────────────────────────────────────────────────────────────
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    name = message.from_user.first_name or "do'stim"
    await message.answer(
        f"🇺🇿\nSalom {name} 👋\n"
        f"@Varoq'ning rasmiy botiga xush kelibsiz\n\n"
        f"⬇ Kontaktingizni yuboring (tugmani bosib)\n\n"
        f"🇺🇸\nHi {name} 👋\n"
        f"Welcome to @Varoq's official bot\n\n"
        f"⬇ Send your contact (by clicking button)",
        reply_markup=CONTACT_KEYBOARD,
    )

# ── /login ───────────────────────────────────────────────────────────────────
@dp.message(Command("login"))
async def login_handler(message: types.Message):
    await message.answer(
        "📱 Kontaktingizni yuboring / Send your contact:",
        reply_markup=CONTACT_KEYBOARD,
    )

# ── Contact handler ─────────────────────────────────────────────────────────
@dp.message(F.contact)
async def contact_handler(message: types.Message):
    contact = message.contact
    if contact.user_id != message.from_user.id:
        await message.answer("❌ Please share your own contact.")
        return

    phone = contact.phone_number.lstrip("+")
    code = str(secrets.randbelow(900000) + 100000)  # 6-digit secure code

    async with pool.acquire() as conn:
        # Mark old codes as used
        await conn.execute(
            "UPDATE otp_codes SET used_at = NOW() WHERE phone = $1 AND used_at IS NULL",
            phone,
        )
        # Create new OTP
        await conn.execute(
            """
            INSERT INTO otp_codes (phone, code, expires_at, chat_id)
            VALUES ($1, $2, NOW() + INTERVAL '5 minutes', $3)
            ON CONFLICT (phone) 
            DO UPDATE SET 
                code = $2,
                expires_at = NOW() + INTERVAL '5 minutes',
                used_at = NULL,
                chat_id = $3
            """,
            phone, code, message.chat.id,
        )

    await message.answer(
        f"🔐 Sizning Varoq kodingiz:\n\n"
        f"`{code}`\n\n"
        f"Kod 5 daqiqa davomida amal qiladi.\n\n"
        f"🇺🇿 Yangi kod olish uchun /login ni bosing\n"
        f"🇺🇸 To get a new code click /login",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )

    # Schedule expiry message
    asyncio.create_task(notify_expiry(message.chat.id, phone, code))

# ── Renew button ────────────────────────────────────────────────────────────
@dp.message(F.text == "🔄 Renew / Yangilash")
async def renew_handler(message: types.Message):
    await login_handler(message)

# ── Expiry notification ─────────────────────────────────────────────────────
async def notify_expiry(chat_id: int, phone: str, code: str):
    await asyncio.sleep(300)  # 5 minutes
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT used_at FROM otp_codes WHERE phone = $1 AND code = $2",
            phone, code
        )
    if row and row["used_at"] is None:
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE otp_codes SET used_at = NOW() WHERE phone = $1 AND code = $2",
                phone, code
            )
        await bot.send_message(
            chat_id,
            "🔒 Kod muddati tugadi. Yangi kod olish uchun /login ni bosing.\n\n"
            "🔒 Code expired. Request a new code by pressing /login",
            reply_markup=RENEW_KEYBOARD,
        )

# ── DB init ─────────────────────────────────────────────────────────────────
async def init_db(conn):
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS otp_codes (
            id SERIAL PRIMARY KEY,
            phone TEXT UNIQUE NOT NULL,
            code TEXT NOT NULL,
            chat_id BIGINT,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            expires_at TIMESTAMPTZ NOT NULL,
            used_at TIMESTAMPTZ
        )
    """)

async def main():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    async with pool.acquire() as conn:
        await init_db(conn)
    print("✅ Varoq Telegram Bot is running...")
    await dp.start_polling(bot)
    await pool.close()

if __name__ == "__main__":
    asyncio.run(main())