import asyncio
import os
import uuid
import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Support both DATABASE_URL directly, or individual DB_* vars (same .env as Django)
DATABASE_URL = os.getenv("DATABASE_URL") or (
    "postgresql://{user}:{password}@{host}:{port}/{name}".format(
        user=os.getenv("DB_USER", "varoq"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        name=os.getenv("DB_NAME", "varoq"),
    )
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message, command: CommandStart):
    session_token = command.args
    print(f"🔍 DEBUG: /start received | session_token = {session_token}")

    if not session_token:
        await message.answer(
            "👋 Varoq botiga xush kelibsiz!\n\n"
            "Kodingizni olish uchun ilovani oching va telefon raqamingizni kiriting."
        )
        return

    # Validate it's actually a UUID before hitting the DB
    try:
        token_uuid = uuid.UUID(session_token)
    except ValueError:
        print(f"❌ Invalid UUID format: {session_token}")
        await message.answer("❌ Havola noto'g'ri. Iltimos, ilovadan yangi kod so'rang.")
        return

    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print(f"✅ Connected to DB for token: {session_token}")

        otp = await conn.fetchrow(
            """
            SELECT id, code FROM otp_codes
            WHERE session_token = $1
              AND used_at IS NULL
              AND expires_at > NOW()
            """,
            token_uuid,  # ← pass as UUID, not string
        )

        if not otp:
            print(f"❌ OTP NOT FOUND for token: {session_token}")
            await message.answer("❌ Havola eskirgan yoki noto'g'ri. Iltimos, ilovadan yangi kod so'rang.")
            return

        print(f"🎉 OTP FOUND → Code = {otp['code']}")

        await conn.execute(
            "UPDATE otp_codes SET chat_id = $1 WHERE id = $2",
            message.chat.id, otp['id'],
        )

        await message.answer(
            f"🔐 Sizning Varoq kodingiz:\n\n"
            f"`{otp['code']}`\n\n"
            f"Kod 5 daqiqa davomida amal qiladi.",
            parse_mode="Markdown",
        )

    except Exception as e:
        print(f"🚨 ERROR: {type(e).__name__}: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")
    finally:
        if 'conn' in locals() and not conn.is_closed():
            await conn.close()


async def main():
    print(f"🚀 Varoq bot starting... DB: {DATABASE_URL.split('@')[-1]}")  # log host only, not password
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())