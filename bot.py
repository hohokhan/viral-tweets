import os
import re
from telegram import Bot, ParseMode
from telegram.error import TelegramError

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_FROM = '@XIXTEST1'
CHANNEL_TO = '@XIXTEST2'
MENTION_TAG = "@XIXTEST2"  # چیزی که پایین هر پست اضافه میشه

bot = Bot(token=BOT_TOKEN)

def clean_text(text):
    if not text:
        return MENTION_TAG
    text = re.sub(r'@\w+', '', text)                     # حذف آیدی‌ها
    text = re.sub(r'https?://t\.me/\S+', '', text)       # حذف لینک‌های t.me
    text = re.sub(r'\n{2,}', '\n', text).strip()         # حذف خطوط خالی اضافی
    return text + "\n\n" + MENTION_TAG

with open("post.txt", "r") as f:
    url = f.read().strip()

match = re.match(r'https://t\.me/[^/]+/(\d+)', url)
if not match:
    raise ValueError("❌ لینک معتبر نیست.")
message_id = int(match.group(1))

try:
    msg = bot.forward_message(chat_id=8049174660, from_chat_id=CHANNEL_FROM, message_id=message_id)

    # صبر کوتاه برای اطمینان از فوروارد شدن
    import time
    time.sleep(1)

    if msg.text:
        text = clean_text(msg.text)
        bot.send_message(chat_id=CHANNEL_TO, text=text, parse_mode=ParseMode.HTML)
        print("✅ پیام متنی ارسال شد.")

    elif msg.caption and msg.photo:
        caption = clean_text(msg.caption)
        bot.send_photo(chat_id=CHANNEL_TO, photo=msg.photo[-1].file_id, caption=caption, parse_mode=ParseMode.HTML)
        print("✅ عکس با کپشن ارسال شد.")

    elif msg.caption and msg.video:
        caption = clean_text(msg.caption)
        bot.send_video(chat_id=CHANNEL_TO, video=msg.video.file_id, caption=caption, parse_mode=ParseMode.HTML)
        print("✅ ویدیو با کپشن ارسال شد.")

    else:
        # اگر متن یا کپشن نداشت، همونطوری کپی کن
        bot.copy_message(chat_id=CHANNEL_TO, from_chat_id=CHANNEL_FROM, message_id=message_id)
        print("ℹ️ پیام ساده کپی شد (بدون متن/کپشن).")

except TelegramError as e:
    print(f"❌ خطا در ارسال پیام: {e}")
    exit(1)

# برو سراغ پیام بعدی
new_url = f"https://t.me/XIXTEST1/{message_id + 1}"
with open("post.txt", "w") as f:
    f.write(new_url)

print(f"📤 post.txt آپدیت شد به {new_url}")
