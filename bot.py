from telegram import Bot
import os
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_FROM = '@XIXTEST1'
CHANNEL_TO = '@XIXTEST2'
MENTION_TAG = '@XIXTEST2'

bot = Bot(token=BOT_TOKEN)

# مرحله 1: خواندن لینک
with open("post.txt", "r") as f:
    url = f.read().strip()

match = re.match(r'https://t\.me/[^/]+/(\d+)', url)
if not match:
    raise ValueError("❌ لینک معتبر نیست.")
message_id = int(match.group(1))

try:
    # مرحله 2: دریافت پیام
    msg = bot.forward_message(chat_id=CHANNEL_TO, from_chat_id=CHANNEL_FROM, message_id=message_id)

    # مرحله 3: تعیین متن نهایی (برای پیام‌های متنی یا کپشن‌دار)
    if msg.text:
        text = re.sub(r'@\w+', '', msg.text)
        text = re.sub(r'https?://t\.me/\S+', '', text).strip()
        final_text = text + "\n\n" + MENTION_TAG
        bot.send_message(chat_id=CHANNEL_TO, text=final_text)
    elif msg.caption and msg.photo:
        text = re.sub(r'@\w+', '', msg.caption)
        text = re.sub(r'https?://t\.me/\S+', '', text).strip()
        final_text = text + "\n\n" + MENTION_TAG
        bot.send_photo(chat_id=CHANNEL_TO, photo=msg.photo[-1].file_id, caption=final_text)
    else:
        # fallback: فقط فوروارد کن
        bot.copy_message(chat_id=CHANNEL_TO, from_chat_id=CHANNEL_FROM, message_id=message_id)

    print(f"✅ پست {message_id} ارسال شد.")

    # مرحله 4: آپدیت لینک در فایل
    new_url = f"https://t.me/XIXTEST1/{message_id + 1}"
    with open("post.txt", "w") as f:
        f.write(new_url)
    print(f"📤 post.txt بروزرسانی شد به: {new_url}")

except Exception as e:
    print(f"❌ خطا در ارسال پیام: {e}")
    exit(1)
