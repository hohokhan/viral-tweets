from telegram import Bot
import os
from urllib.parse import urlparse
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_FROM = '@XIXTEST1'
CHANNEL_TO = '@XIXTEST2'

bot = Bot(token=BOT_TOKEN)

with open("post.txt", "r") as f:
    url = f.read().strip()

match = re.match(r'https://t\.me/[^/]+/(\d+)', url)
if not match:
    raise ValueError("لینک معتبر نیست")
message_id = int(match.group(1))

try:
    bot.copy_message(chat_id=CHANNEL_TO, from_chat_id=CHANNEL_FROM, message_id=message_id)
    print(f"پست {message_id} ارسال شد.")
except Exception as e:
    print(f"خطا در ارسال پیام: {e}")
    exit(1)

new_url = f"https://t.me/XIXTEST1/{message_id + 1}"
with open("post.txt", "w") as f:
    f.write(new_url)
