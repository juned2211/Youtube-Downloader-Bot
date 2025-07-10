from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio
)
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.types import CallbackQuery
import youtube_dl

@Client.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data

    if data.startswith("yt_audio|"):
        url = data.split("|", 1)[1]
        await callback_query.answer("Downloading audio...", show_alert=False)
        await callback_query.message.edit("🔄 Downloading audio...")

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                title = info_dict.get("title", "Audio")

            await callback_query.message.reply_audio(
                audio=file_path,
                caption=f"🎵 **{title}**"
            )
            await callback_query.message.delete()

        except Exception as e:
            await callback_query.message.edit(f"❌ Error downloading audio:\n`{str(e)}`")

    elif data.startswith("yt_video|"):
        url = data.split("|", 1)[1]
        await callback_query.answer("Downloading video...", show_alert=False)
        await callback_query.message.edit("🔄 Downloading video...")

        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'quiet': True,
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info_dict)
                title = info_dict.get("title", "Video")

            await callback_query.message.reply_video(
                video=file_path,
                caption=f"🎬 **{title}**"
            )
            await callback_query.message.delete()

        except Exception as e:
            await callback_query.message.edit(f"❌ Error downloading video:\n`{str(e)}`")
