import os
import re
import asyncio
from telegram import Bot
from telegram.constants import ParseMode

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_FROM = '@XIXTEST1'
CHANNEL_TO = '@XIXTEST2'  # آیدی کانال مقصدت
MENTION_TAG = "@XIXTEST2"  # چیزی که می‌خوای اضافه بشه

def clean_text(text):
    if not text:
        return MENTION_TAG
    # حذف @username
    text = re.sub(r'@\w+', '', text)
    # حذف لینک‌های t.me
    text = re.sub(r'https?://t\.me/\S+', '', text)
    # حذف فاصله‌های اضافی
    text = re.sub(r'\n{2,}', '\n', text).strip()
    return text + "\n\n" + MENTION_TAG

async def main():
    bot = Bot(token=BOT_TOKEN)

    with open("post.txt", "r") as f:
        url = f.read().strip()

    match = re.match(r'https://t\.me/[^/]+/(\d+)', url)
    if not match:
        raise ValueError("لینک معتبر نیست")
    message_id = int(match.group(1))

    try:
        message = await bot.get_chat(CHANNEL_FROM)
        message = await bot.get_message(chat_id=CHANNEL_FROM, message_id=message_id)

        if message.caption:
            clean_caption = clean_text(message.caption)
        else:
            clean_caption = MENTION_TAG

        if message.text:
            clean_text_msg = clean_text(message.text)

        if message.photo:
            await bot.send_photo(
                chat_id=CHANNEL_TO,
                photo=message.photo[-1].file_id,
                caption=clean_caption,
                parse_mode=ParseMode.HTML
            )
        elif message.video:
            await bot.send_video(
                chat_id=CHANNEL_TO,
                video=message.video.file_id,
                caption=clean_caption,
                parse_mode=ParseMode.HTML
            )
        elif message.text:
            await bot.send_message(
                chat_id=CHANNEL_TO,
                text=clean_text_msg,
                parse_mode=ParseMode.HTML
            )
        else:
            print("فرمت پیام پشتیبانی نمی‌شود، استفاده از copy_message")
            await bot.copy_message(chat_id=CHANNEL_TO, from_chat_id=CHANNEL_FROM, message_id=message_id)

        print(f"پست {message_id} ارسال شد.")

    except Exception as e:
        print(f"خطا در ارسال پیام: {e}")
        exit(1)

    # آپدیت فایل
    new_url = f"https://t.me/XIXTEST1/{message_id + 1}"
    with open("post.txt", "w") as f:
        f.write(new_url)

if __name__ == "__main__":
    asyncio.run(main())
