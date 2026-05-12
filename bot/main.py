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

CONTACT_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Kontaktingizni yuboring", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

RENEW_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔄 Yangilash / Renew")]],
    resize_keyboard=True,
)


# ── Shared: generate OTP and send ────────────────────────────────────────────
async def generate_and_send_code(message: types.Message, phone: str):
    code = str(secrets.randbelow(900000) + 100000)

    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE otp_codes SET used_at = NOW() WHERE phone = $1 AND used_at IS NULL",
            phone,
        )
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

    asyncio.create_task(notify_expiry(message.chat.id, phone, code))


# ── /start ────────────────────────────────────────────────────────────────────
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    name = message.from_user.first_name or "do'stim"
    chat_id = message.chat.id

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT phone FROM otp_codes WHERE chat_id = $1 ORDER BY created_at DESC LIMIT 1",
            chat_id,
        )

    if row:
        await generate_and_send_code(message, row["phone"])
    else:
        await message.answer(
            f"🇺🇿\nSalom {name} 👋\n"
            f"@Varoq'ning rasmiy botiga xush kelibsiz\n\n"
            f"⬇ Kontaktingizni yuboring (tugmani bosib)\n\n"
            f"🇺🇸\nHi {name} 👋\n"
            f"Welcome to @Varoq's official bot\n\n"
            f"⬇ Send your contact (by clicking button)",
            reply_markup=CONTACT_KEYBOARD,
        )


# ── /login ────────────────────────────────────────────────────────────────────
@dp.message(Command("login"))
async def login_handler(message: types.Message):
    chat_id = message.chat.id

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT phone FROM otp_codes WHERE chat_id = $1 ORDER BY created_at DESC LIMIT 1",
            chat_id,
        )

    if row:
        await generate_and_send_code(message, row["phone"])
    else:
        await message.answer(
            "📱 Kontaktingizni yuboring / Send your contact:",
            reply_markup=CONTACT_KEYBOARD,
        )


# ── Contact shared ────────────────────────────────────────────────────────────
@dp.message(F.contact)
async def contact_handler(message: types.Message):
    try:
        contact = message.contact
        if contact.user_id != message.from_user.id:
            await message.answer("❌ Please share your own contact.")
            return

        phone = contact.phone_number.lstrip("+")
        await generate_and_send_code(message, phone)

    except Exception as e:
        print(f"❌ ERROR in contact_handler: {type(e).__name__}: {e}", flush=True)
        await message.answer("❌ Xatolik yuz berdi. Iltimos /login ni bosing va qayta urinib ko'ring.")


# ── Renew button ──────────────────────────────────────────────────────────────
@dp.message(F.text == "🔄 Yangilash / Renew")
async def renew_handler(message: types.Message):
    await login_handler(message)


# ── Expiry notification ───────────────────────────────────────────────────────
async def notify_expiry(chat_id: int, phone: str, code: str):
    await asyncio.sleep(300)
    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT used_at FROM otp_codes WHERE phone = $1 AND code = $2",
                phone, code,
            )
            if row and row["used_at"] is None:
                await conn.execute(
                    "UPDATE otp_codes SET used_at = NOW() WHERE phone = $1 AND code = $2",
                    phone, code,
                )
        await bot.send_message(
            chat_id,
            "🔒 Kod muddati tugadi. Yangi kod olish uchun /login ni bosing.\n\n"
            "🔒 Code expired. Request a new code by pressing /login",
            reply_markup=RENEW_KEYBOARD,
        )
    except Exception as e:
        print(f"❌ ERROR in notify_expiry: {e}", flush=True)


# ── Main ──────────────────────────────────────────────────────────────────────
async def main():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    print("✅ Varoq Telegram Bot is running...", flush=True)
    await dp.start_polling(bot)
    await pool.close()


if __name__ == "__main__":
    asyncio.run(main())