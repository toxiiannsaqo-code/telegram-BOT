import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

BOT_TOKEN = "8518976130:AAFyq2yxPek0O7B9l50LTGhYRTyei6N2AG8"  # вставь свой токен

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

students = [
    "Abramyan Araik", "Adamyan Slava", "Badalyan Arman", "Gazarov Artur", "Gevorgyan Artyom", "Grigoryan Grigori",
    "Grigoryan Taron", "Toxyan Sargis", "Xachatryan Edik", "Tsaturyan Gor", "Hakobyan Mher", "Harutyunyan Hrant",
    "Harutyunyan Seyran", "Hovhannisyan Hovik", "Melqonyan Zohrab", "Mkrtchyan Tigran", "Petrosyan Aram",
    "Petrosyan Artur", "Soghomonyan Gagik", "Stepanyan Narek"
]

attendance_data = {}


def get_keyboard(present_list):
    """Создаёт клавиатуру с кнопками учеников"""
    keyboard = []
    row = []
    for name in students:
        mark = "✅" if name in present_list else "❌"
        row.append(InlineKeyboardButton(text=f"{mark} {name}", callback_data=name))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton(text="📊 Ցույց տալ արդյունքը", callback_data="result")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message(Command(commands=["start"]))
async def start_cmd(message: types.Message):
    teacher_id = message.from_user.id
    attendance_data[teacher_id] = set()
    await message.answer(
        "Բարև! Նշիր ներկաներին՝ սեղմելով անունների վրա.\nԵրբ ավարտես՝ սեղմիր 📊 «Ցույց տալ արդյունքը». ",
        reply_markup=get_keyboard(attendance_data[teacher_id])
    )


@dp.callback_query()
async def process_callback(callback: types.CallbackQuery):
    teacher_id = callback.from_user.id

    if teacher_id not in attendance_data:
        attendance_data[teacher_id] = set()

    if callback.data == "result":
        present = list(attendance_data[teacher_id])
        absent = [s for s in students if s not in present]

        text = (
            f"📋 Արդյունք:\n\n"
            f"✅ Ներկա են ({len(present)}): {', '.join(present) or '—'}\n\n"
            f"❌ Բացակա են ({len(absent)}): {', '.join(absent) or '—'}"
        )

        await callback.message.edit_text(text)
    else:
        name = callback.data
        if name in attendance_data[teacher_id]:
            attendance_data[teacher_id].remove(name)
        else:
            attendance_data[teacher_id].add(name)

        await callback.message.edit_reply_markup(reply_markup=get_keyboard(attendance_data[teacher_id]))

    await callback.answer()


async def main():
    print("✅ Բոտը գործարկված է։ Բացիր Telegram-ը և գրիր նրան /start։")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

