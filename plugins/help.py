from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(["start", "help"]))
async def start(_, message: Message):
    await message.reply_text(
        f"👋 Hello {message.from_user.mention},\n\n"
        "Send me any **YouTube video link**, and I'll give you download options.\n\n"
        "**Supported formats:**\n"
        "- 🎥 Video (various resolutions)\n"
        "- 🎵 Audio (MP3)\n\n"
        "✅ No watermark\n"
        "⚡ Fast processing\n"
        "🛠 Made by Juned"
    )
