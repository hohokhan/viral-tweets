import os
import re
from telegram import Bot
from telegram.error import TelegramError

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_FROM = '@XIXTEST1'
CHANNEL_TO = '@XIXTEST2'
MENTION_TAG = '@XIXTEST2'

bot = Bot(token=BOT_TOKEN)

def clean_text(text):
    if not text:
        return MENTION_TAG
    # حذف @username و لینک‌های t.me
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'https?://t\.me/\S+', '', text)
    text = re.sub(r'\n{2,}', '\n', text).strip()
    return text + "\n\n" + MENTION_TAG

def main():
    # خواندن لینک از فایل
    with open("post.txt", "r") as f:
        url = f.read().strip()

    match = re.match(r'https://t\.me/[^/]+/(\d+)', url)
    if not match:
        print("❌ لینک معتبر نیست.")
        return

    message_id = int(match.group(1))
    print(f"📥 پیام در حال پردازش: {message_id}")

    try:
        # پیام رو به صورت موقت برای پردازش فوروارد می‌کنیم به خودمون
        temp_chat_id = 8049174660  # آیدی عددی خودت
        temp_msg = bot.forward_message(chat_id=temp_chat_id, from_chat_id=CHANNEL_FROM, message_id=message_id)

        # صبر می‌کنیم مطمئن بشیم پیام رسید
        import time
        time.sleep(1)

        # بررسی نوع پیام و ارسال با متن پاک‌شده
        if temp_msg.text:
            final_text = clean_text(temp_msg.text)
            bot.send_message(chat_id=CHANNEL_TO, text=final_text)
            print("✅ پیام متنی ارسال شد.")

        elif temp_msg.caption and temp_msg.photo:
            final_text = clean_text(temp_msg.caption)
            bot.send_photo(chat_id=CHANNEL_TO, photo=temp_msg.photo[-1].file_id, caption=final_text)
            print("✅ عکس با کپشن ارسال شد.")

        elif temp_msg.caption and temp_msg.video:
            final_text = clean_text(temp_msg.caption)
            bot.send_video(chat_id=CHANNEL_TO, video=temp_msg.video.file_id, caption=final_text)
            print("✅ ویدیو با کپشن ارسال شد.")

        else:
            print("ℹ️ پیام پشتیبانی نمی‌شود، ارسال نشد.")
            return

        # آپدیت فایل فقط در صورت ارسال موفق
        new_url = f"https://t.me/XIXTEST1/{message_id + 1}"
        with open("post.txt", "w") as f:
            f.write(new_url)
        print(f"📤 post.txt آپدیت شد به: {new_url}")

    except TelegramError as e:
        print(f"❌ خطا در ارسال: {e}")

if __name__ == "__main__":
    main()
