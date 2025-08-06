import os
import re
from telegram import Bot, ParseMode

# توکن و کانال‌ها
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_FROM = '@XIXTEST1'
CHANNEL_TO = '@XIXTEST2'  # ← آیدی کانال مقصد
MENTION_TAG = "@XIXTEST2"  # ← تگ کانال مقصد که باید به پست اضافه بشه

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

def main():
    print("⏳ شروع عملیات...")

    bot = Bot(token=BOT_TOKEN)

    # خواندن لینک از فایل
    with open("post.txt", "r") as f:
        url = f.read().strip()

    print(f"📥 لینک فعلی: {url}")

    # استخراج شماره پیام
    match = re.match(r'https://t\.me/[^/]+/(\d+)', url)
    if not match:
        raise ValueError("❌ لینک معتبر نیست.")
    message_id = int(match.group(1))
    print(f"🔍 ID پیام: {message_id}")

    try:
        # دریافت پیام از کانال مبدا
        message = bot.forward_message(chat_id='@YourTempBot', from_chat_id=CHANNEL_FROM, message_id=message_id)
        msg = bot.get_chat(CHANNEL_FROM).get_message(message_id)

        # دریافت نوع پیام
        if msg.photo:
            caption = clean_text(msg.caption)
            bot.send_photo(
                chat_id=CHANNEL_TO,
                photo=msg.photo[-1].file_id,
                caption=caption,
                parse_mode=ParseMode.HTML
            )
            print("✅ ارسال عکس با کپشن انجام شد.")
        elif msg.video:
            caption = clean_text(msg.caption)
            bot.send_video(
                chat_id=CHANNEL_TO,
                video=msg.video.file_id,
                caption=caption,
                parse_mode=ParseMode.HTML
            )
            print("✅ ارسال ویدیو با کپشن انجام شد.")
        elif msg.text:
            text = clean_text(msg.text)
            bot.send_message(
                chat_id=CHANNEL_TO,
                text=text,
                parse_mode=ParseMode.HTML
            )
            print("✅ ارسال متن انجام شد.")
        else:
            # fallback به فوروارد ساده
            bot.copy_message(chat_id=CHANNEL_TO, from_chat_id=CHANNEL_FROM, message_id=message_id)
            print("ℹ️ فرمت خاص، پیام فوروارد شد.")

    except Exception as e:
        print(f"❌ خطا در ارسال: {e}")
        return

    # آپدیت فایل post.txt برای پیام بعدی
    next_message_id = message_id + 1
    new_url = f"https://t.me/XIXTEST1/{next_message_id}"
    with open("post.txt", "w") as f:
        f.write(new_url)
    print(f"📤 post.txt آپدیت شد به {new_url}")

if __name__ == "__main__":
    main()
