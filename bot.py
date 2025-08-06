import os
import re
import time
from telegram import Bot
from telegram.error import TelegramError

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_FROM = '@XIXTEST1'
CHANNEL_TO = '@XIXTEST2'
MENTION_TAG = '@XIXTEST2'
TEMP_CHAT_ID = 8049174660  # آیدی عددی خودت

bot = Bot(token=BOT_TOKEN)

def clean_text(text):
    if not text:
        return MENTION_TAG
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'https?://t\.me/\S+', '', text)
    text = re.sub(r'\n{2,}', '\n', text).strip()
    return text + "\n\n" + MENTION_TAG

def main():
    try:
        with open("post.txt", "r") as f:
            url = f.read().strip()
        print(f"📥 URL از فایل: {url}")
    except FileNotFoundError:
        print("❌ فایل post.txt پیدا نشد.")
        return

    match = re.match(r'https://t\.me/[^/]+/(\d+)', url)
    if not match:
        print("❌ لینک معتبر نیست.")
        return

    message_id = int(match.group(1))
    print(f"🔢 message_id: {message_id}")

    try:
        msg = bot.forward_message(chat_id=TEMP_CHAT_ID, from_chat_id=CHANNEL_FROM, message_id=message_id)
        time.sleep(1)

        sent = False

        if msg.text:
            cleaned = clean_text(msg.text)
            bot.send_message(chat_id=CHANNEL_TO, text=cleaned)
            sent = True
            print("✅ پیام متنی ارسال شد.")

        elif msg.caption and msg.photo:
            cleaned = clean_text(msg.caption)
            bot.send_photo(chat_id=CHANNEL_TO, photo=msg.photo[-1].file_id, caption=cleaned)
            sent = True
            print("✅ عکس ارسال شد.")

        elif msg.caption and msg.video:
            cleaned = clean_text(msg.caption)
            bot.send_video(chat_id=CHANNEL_TO, video=msg.video.file_id, caption=cleaned)
            sent = True
            print("✅ ویدیو ارسال شد.")

        else:
            print("ℹ️ فرمت پیام پشتیبانی نمی‌شود.")
            return

        # فقط اگر ارسال موفق بود فایل آپدیت میشه
        if sent:
            new_url = f"https://t.me/XIXTEST1/{message_id + 1}"
            with open("post.txt", "w") as f:
                f.write(new_url)
            print(f"📤 فایل post.txt آپدیت شد به: {new_url}")
        else:
            print("⚠️ ارسال موفق نبود، فایل آپدیت نشد.")

    except TelegramError as e:
        print(f"❌ خطای تلگرام: {e}")

if __name__ == "__main__":
    main()
