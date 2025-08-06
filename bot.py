import os
import re
import subprocess
import time
from telegram import Bot, ParseMode
from telegram.error import TelegramError

# تنظیمات
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_FROM = '@PHISHTE'  # کانال مبدا - می‌تونه خصوصی هم باشه
CHANNEL_TO = '@XIXTEST2'   # کانال مقصد
MENTION_TAG = "@XIXTEST2"  # تگ نهایی
TEMP_CHAT_ID = 8049174660  # آیدی عددی برای تست پیام

bot = Bot(token=BOT_TOKEN)

def clean_text(text):
    if not text:
        return MENTION_TAG
    # حذف @username‌ها
    text = re.sub(r'@\w+', '', text)
    # حذف لینک‌های t.me
    text = re.sub(r'https?://t\.me/\S+', '', text)
    return text.strip() + "\n" + MENTION_TAG

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

    # خواندن لینک از post.txt
    with open("post.txt", "r") as f:
        url = f.read().strip()
    print(f"📥 URL از فایل: {url}")

    match = re.match(r'https://t\.me/[^/]+/(\d+)', url)
    if not match:
        raise ValueError("❌ لینک معتبر نیست.")
    message_id = int(match.group(1))
    print(f"🔢 message_id: {message_id}")

    try:
        # فوروارد پیام برای دریافت اطلاعاتش
        msg = bot.forward_message(chat_id=TEMP_CHAT_ID, from_chat_id=CHANNEL_FROM, message_id=message_id)
        time.sleep(1)

        # پردازش انواع پیام‌ها
        if msg.text:
            cleaned = clean_text(msg.text)
            bot.send_message(chat_id=CHANNEL_TO, text=cleaned, parse_mode=ParseMode.HTML)
            print("✅ پیام متنی ارسال شد.")

        elif msg.photo:
            caption = clean_text(msg.caption) if msg.caption else MENTION_TAG
            bot.send_photo(chat_id=CHANNEL_TO, photo=msg.photo[-1].file_id, caption=caption, parse_mode=ParseMode.HTML)
            print("✅ عکس ارسال شد.")

        elif msg.video:
            caption = clean_text(msg.caption) if msg.caption else MENTION_TAG
            bot.send_video(chat_id=CHANNEL_TO, video=msg.video.file_id, caption=caption, parse_mode=ParseMode.HTML)
            print("✅ ویدیو ارسال شد.")

        elif msg.animation:
            caption = clean_text(msg.caption) if msg.caption else MENTION_TAG
            bot.send_animation(chat_id=CHANNEL_TO, animation=msg.animation.file_id, caption=caption, parse_mode=ParseMode.HTML)
            print("✅ گیف ارسال شد.")

        elif msg.audio:
            caption = clean_text(msg.caption) if msg.caption else MENTION_TAG
            bot.send_audio(chat_id=CHANNEL_TO, audio=msg.audio.file_id, caption=caption, parse_mode=ParseMode.HTML)
            print("✅ صدا ارسال شد.")

        else:
            # سایر پیام‌ها فقط copy می‌شن
            bot.copy_message(chat_id=CHANNEL_TO, from_chat_id=CHANNEL_FROM, message_id=message_id)
            print("ℹ️ پیام فوروارد شد (نوع ناشناخته).")

    except TelegramError as e:
        print(f"❌ خطا در ارسال: {e}")
        return

    # آپدیت post.txt برای پیام بعدی
    next_message_id = message_id + 1
    new_url = f"https://t.me/XIXTEST1/{next_message_id}"  # فقط message_id عوض می‌شه
    with open("post.txt", "w") as f:
        f.write(new_url)
    print(f"📤 فایل post.txt آپدیت شد به: {new_url}")

    # Git commit & push
    git_commit_push()

if __name__ == "__main__":
    main()
