from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import youtube_dl

@Client.on_message(filters.command("yt") & filters.private)
async def download_youtube(_, message: Message):
    if len(message.command) < 2:
        await message.reply("❌ Please provide a valid YouTube link.\n\nExample:\n`/yt https://youtu.be/xxxxxx`")
        return

    url = message.text.split(maxsplit=1)[1]
    msg = await message.reply("🔍 Fetching download info...")

    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail')
            formats = info.get('formats', [])

        buttons = []
        for f in formats:
            if f.get("filesize") and f.get("url") and f.get("ext") == "mp4":
                size = round(f["filesize"] / 1024 / 1024, 2)
                quality = f.get("format_note", f.get("format_id"))
                buttons.append([
                    InlineKeyboardButton(
                        f"{quality} - {size} MB",
                        url=f["url"]
                    )
                ])

        if not buttons:
            await msg.edit("⚠️ No downloadable formats found.")
            return

        await msg.delete()
        await message.reply_photo(
            photo=thumbnail,
            caption=f"🎬 **{title}**\n\nSelect format to download:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except Exception as e:
        await msg.edit(f"❌ Error:\n`{str(e)}`")
