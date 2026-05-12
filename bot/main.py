import asyncio
import os
import random
from datetime import datetime, timedelta

import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

pool: asyncpg.Pool | None = None

# Contact button
contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Kontaktingizni yuboring", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user = message.from_user
    first_name = user.first_name or "do'stim"

    await message.answer(
        f"🇺🇿\nSalom {first_name} 👋\n"
        f"@Varoq'ning rasmiy botiga xush kelibsiz\n\n"
        f"⬇ Kontaktingizni yuboring (tugmani bosib)\n\n"
        f"🇺🇸\nHi {first_name} 👋\n"
        f"Welcome to @Varoq's official bot\n\n"
        f"⬇ Send your contact (by clicking button)",
        reply_markup=contact_keyboard
    )


@dp.message(types.ContentType.CONTACT)
async def contact_handler(message: types.Message):
    if not message.contact or not message.contact.phone_number:
        await message.answer("❌ Contact not received. Please try again.")
        return

    phone = message.contact.phone_number.lstrip("+")  # normalize
    chat_id = message.chat.id

    # Generate 6-digit OTP (you can also call Django /send_otp if you prefer)
    code = f"{random.randint(100000, 999999)}"
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    async with pool.acquire() as conn:
        # Upsert OTP for this phone (matches your existing otp_codes table)
        await conn.execute(
            """
            INSERT INTO otp_codes (phone, code, expires_at, chat_id, used_at, session_token)
            VALUES ($1, $2, $3, $4, NULL, NULL)
            ON CONFLICT (phone) DO UPDATE 
            SET code = $2, expires_at = $3, chat_id = $4, used_at = NULL
            """,
            phone, code, expires_at, chat_id
        )

    await message.answer(
        f"🔐 Sizning Varoq kodingiz:\n\n"
        f"`{code}`\n\n"
        f"Kod 5 daqiqa davomida amal qiladi.\n\n"
        f"🇺🇿 Yangi kod olish uchun /login ni bosing\n"
        f"🇺🇸 To get a new code click /login",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Command("login"))
async def login_handler(message: types.Message):
    await message.answer(
        "🔑 Yangi kod olish uchun kontaktingizni yuboring 👇",
        reply_markup=contact_keyboard
    )


# Optional: simple expiration handler (you can expand with scheduler)
@dp.message()
async def echo(message: types.Message):
    if "kod" in message.text.lower() or "code" in message.text.lower():
        await message.answer("Kod muddati tugadi? /login ni bosing va yangi kod oling!")


async def main():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    print("✅ Varoq Telegram bot is running...")
    await dp.start_polling(bot)
    await pool.close()


if __name__ == "__main__":
    asyncio.run(main())