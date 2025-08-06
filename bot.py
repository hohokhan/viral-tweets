import os
import re
import subprocess
import time
from telegram import Bot, ParseMode
from telegram.error import TelegramError

# تنظیمات
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_FROM = '@XIXTEST1'
CHANNEL_TO = '@XIXTEST2'
MENTION_TAG = "ــــــــــ @XIXTEST2 ــــــــــ"
TEMP_CHAT_ID = 8049174660  # آیدی عددی خودت یا گروه تست

bot = Bot(token=BOT_TOKEN)

def clean_text(text):
    if not text:
        return MENTION_TAG
    # حذف @username
    text = re.sub(r'@\w+', '', text)
    # حذف لینک‌های t.me
    text = re.sub(r'https?://t\.me/\S+', '', text)
    # حذف فاصله‌های اضافه
    text = re.sub(r'\n{2,}', '\n', text).strip()
    return text + "\n\n" + MENTION_TAG

def git_commit_push():
    try:
        subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "add", "post.txt"], check=True)
        subprocess.run(["git", "commit", "-m", "⬆️ update post.txt"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ فایل post.txt با موفقیت push شد.")
    except subprocess.CalledProcessError as e:
        print(f"❌ خطا در git push: {e}")

def main():
    print("⏳ شروع عملیات...")

    # خواندن لینک فعلی
    with open("post.txt", "r") as f:
        url = f.read().strip()

    print(f"📥 URL از فایل: {url}")

    match = re.match(r'https://t\.me/[^/]+/(\d+)', url)
    if not match:
        raise ValueError("❌ لینک معتبر نیست.")
    message_id = int(match.group(1))
    print(f"🔢 message_id: {message_id}")

    try:
        # فوروارد موقت برای دریافت محتوای پیام
        msg = bot.forward_message(chat_id=TEMP_CHAT_ID, from_chat_id=CHANNEL_FROM, message_id=message_id)
        time.sleep(1)

        # بررسی نوع پیام
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
            # اگر نوعی نبود که بشه تمیز کرد، فقط copy کن
            bot.copy_message(chat_id=CHANNEL_TO, from_chat_id=CHANNEL_FROM, message_id=message_id)
            print("ℹ️ پیام فوروارد شد (نوع ناشناخته).")

    except TelegramError as e:
        print(f"❌ خطا در ارسال: {e}")
        return

    # آپدیت post.txt
    next_message_id = message_id + 1
    new_url = f"https://t.me/XIXTEST1/{next_message_id}"
    with open("post.txt", "w") as f:
        f.write(new_url)
    print(f"📤 فایل post.txt آپدیت شد به: {new_url}")

    # Git commit و push فایل
    git_commit_push()

if __name__ == "__main__":
    main()
