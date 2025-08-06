import os
import re
from telegram import Bot, ParseMode
from telegram.error import TelegramError

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_FROM = '@XIXTEST1'
CHANNEL_TO = '@XIXTEST2'
MENTION_TAG = "@XIXTEST2"

def clean_text(text):
    if not text:
        return MENTION_TAG
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'https?://t\.me/\S+', '', text)
    text = re.sub(r'\n{2,}', '\n', text).strip()
    return text + "\n\n" + MENTION_TAG

def main():
    print("⏳ شروع عملیات...")

    bot = Bot(token=BOT_TOKEN)

    # خواندن لینک از فایل
    with open("post.txt", "r") as f:
        url = f.read().strip()
    print(f"📥 لینک فعلی: {url}")

    match = re.match(r'https://t\.me/[^/]+/(\d+)', url)
    if not match:
        raise ValueError("❌ لینک معتبر نیست.")
    message_id = int(match.group(1))
    print(f"🔍 ID پیام: {message_id}")

    try:
        # دریافت پیام با copy
        msg = bot.copy_message(
            chat_id=CHANNEL_TO,
            from_chat_id=CHANNEL_FROM,
            message_id=message_id
        )
        print("✅ پیام با موفقیت منتقل شد.")
    except TelegramError as e:
        print(f"❌ خطا در ارسال: {e}")
        return

    # آپدیت post.txt
    next_message_id = message_id + 1
    new_url = f"https://t.me/XIXTEST1/{next_message_id}"
    with open("post.txt", "w") as f:
        f.write(new_url)
    print(f"📤 post.txt آپدیت شد به {new_url}")

if __name__ == "__main__":
    main()
