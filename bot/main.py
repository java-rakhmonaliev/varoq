import asyncio
import os
import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message, command: CommandStart):
    session_token = command.args

    if not session_token:
        await message.answer(
            "👋 Varoq botiga xush kelibsiz!\n\n"
            "Kodingizni olish uchun ilovani oching va telefon raqamingizni kiriting."
        )
        return

    conn = await asyncpg.connect(DATABASE_URL)
    try:
        otp = await conn.fetchrow(
            """
            SELECT id, code FROM otp_codes
            WHERE session_token = $1
              AND used_at IS NULL
              AND expires_at > NOW()
            """,
            session_token,
        )

        if not otp:
            await message.answer("❌ Havola eskirgan. Iltimos, ilovadan yangi kod so'rang.")
            return

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
    finally:
        await conn.close()


async def main():
    print("Varoq bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

