from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

@Client.on_message(filters.command("start"))
async def start(_, message: Message):
    buttons = [
        [
            InlineKeyboardButton("📥 Try Now", url="https://t.me/YOUR_BOT_USERNAME_HERE"),
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/YOUR_TELEGRAM_USERNAME_HERE")
        ]
    ]
    await message.reply_photo(
        photo="https://telegra.ph/file/7fe8f7ff1a5f17196e62f.jpg",  # replace with your thumbnail if needed
        caption=f"👋 Hello {message.from_user.mention}!\n\n"
                "Send me any YouTube video link and I'll fetch the download options for you.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
