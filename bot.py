import os
import re
import time
from telegram import Bot, ParseMode
from telegram.error import TelegramError

# توکن ربات و کانال‌ها
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_TO = '@XIXTEST2'
MENTION_TAG = "@XIXTEST2"

# آی‌دی عددی چت موقت (مثلاً آی‌دی خودت یا گروهی که ربات توش ادمینه)
TEMP_CHAT_ID = 8049174660  # ← آیدی عددی خودت یا گروه

def clean_text(text):
    if not text:
        return MENTION_TAG
    text = re.sub(r'@\w+', '', text)  # حذف @username
    text = re.sub(r'https?://t\.me/\S+', '', text)  # حذف لینک‌های t.me
    text = re.sub(r'\n{2,}', '\n', text).strip()  # حذف خطوط خالی اضافی
    return text + "\n\n" + MENTION_TAG  # اضافه‌کردن تگ کانال

def main():
    print("⏳ شروع عملیات...")

    bot = Bot(token=BOT_TOKEN)

    # خواندن لینک از فایل
    with open("post.txt", "r") as f:
        url = f.read().strip()

    print(f"📥 لینک فعلی: {url}")

    # استخراج آیدی پیام از لینک
    match = re.match(r'https://t\.me/[^/]+/(\d+)', url)
    if not match:
        raise ValueError("❌ لینک معتبر نیست.")
    message_id = int(match.group(1))
    print(f"🔍 ID پیام: {message_id}")

    try:
        # فوروارد به چت موقت برای دریافت محتوا
        msg = bot.forward_message(chat_id=TEMP_CHAT_ID, from_chat_id=url.split('/')[3], message_id=message_id)

        # منتظر می‌مونیم تا فوروارد کامل بشه
        time.sleep(1)

        if msg.text:
            cleaned = clean_text(msg.text)
            bot.send_message(chat_id=CHANNEL_TO, text=cleaned, parse_mode=ParseMode.HTML)
            print("✅ پیام متنی ارسال شد.")

        elif msg.caption and msg.photo:
            cleaned = clean_text(msg.caption)
            bot.send_photo(chat_id=CHANNEL_TO, photo=msg.photo[-1].file_id, caption=cleaned, parse_mode=ParseMode.HTML)
            print("✅ عکس با کپشن ارسال شد.")

        elif msg.caption and msg.video:
            cleaned = clean_text(msg.caption)
            bot.send_video(chat_id=CHANNEL_TO, video=msg.video.file_id, caption=cleaned, parse_mode=ParseMode.HTML)
            print("✅ ویدیو با کپشن ارسال شد.")

        else:
            print("ℹ️ نوع پیام پشتیبانی نمی‌شود، فوروارد ساده انجام می‌شود.")
            bot.copy_message(chat_id=CHANNEL_TO, from_chat_id=url.split('/')[3], message_id=message_id)

    except TelegramError as e:
        print(f"❌ خطا در ارسال: {e}")
        return

    # آپدیت post.txt با لینک بعدی
    next_message_id = message_id + 1
    channel_username = re.search(r'https://t\.me/([^/]+)/\d+', url).group(1)
    new_url = f"https://t.me/{channel_username}/{next_message_id}"
    with open("post.txt", "w") as f:
        f.write(new_url)
    print(f"📤 post.txt آپدیت شد به {new_url}")

if __name__ == "__main__":
    main()
