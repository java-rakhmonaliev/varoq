import asyncio
import os
import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.filters.command import CommandObject  # ← correct import

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

pool: asyncpg.Pool | None = None


@dp.message(CommandStart())
async def start_handler(message: types.Message, command: CommandObject):  # ← fixed type
    session_token = command.args

    if not session_token:
        await message.answer(
            "👋 Varoq botiga xush kelibsiz!\n\n"
            "Kodingizni olish uchun ilovani oching va telefon raqamingizni kiriting."
        )
        return

    async with pool.acquire() as conn:
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


async def main():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    print("Varoq bot is running...")
    await dp.start_polling(bot)
    await pool.close()


if __name__ == "__main__":
    asyncio.run(main())