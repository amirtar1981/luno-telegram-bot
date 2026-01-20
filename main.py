import telebot
import random
import time

BOT_TOKEN = "8510729176:AAHMfQdZPc3F8u4wzNzusEev9B-ma9vBA40"
bot = telebot.TeleBot(BOT_TOKEN)

# ===== حافظه کوتاه‌مدت (در RAM) =====
user_state = {}  # user_id -> dict

WELCOME_TEXT = (
    "من لونو هستم 🌙\n"
    "اینجا جای امن حرف زدنه.\n\n"
    "هر چی تو دلت هست، آروم بنویس."
)

# ===== دیتای احساسی =====
MOODS = {
    "sad": ["غم", "ناراحت", "depressed", "sad", "دلگیر"],
    "angry": ["عصبانی", "خشم", "angry", "mad"],
    "anxious": ["استرس", "نگران", "اضطراب", "anxious"],
    "lonely": ["تنها", "lonely", "بی‌کسی"],
    "fear": ["می‌ترسم", "ترس", "fear"]
}

RESPONSES = {
    "sad": [
        "به نظر میاد غمگینی… دوست داری بیشترش رو بگی؟",
        "این حس می‌تونه خیلی سنگین باشه. من گوش می‌کنم.",
        "حق داری اینطوری حس کنی. از کی شروع شد؟"
    ],
    "angry": [
        "عصبانیتت قابل درکه. چی بیشترین فشار رو آورده؟",
        "به نظر خیلی درگیری. می‌خوای خالیش کنی؟"
    ],
    "anxious": [
        "نگرانی می‌تونه خسته‌کننده باشه. الان بدنت چه حسی داره؟",
        "به نظر مضطربی… همین‌جا می‌تونیم آروم حرف بزنیم."
    ],
    "lonely": [
        "تنهایی سخته… الان تنها نیستی 🤍",
        "خوبه که گفتیش. من اینجام."
    ],
    "fear": [
        "ترس واقعی و جدیه. می‌خوای بگی از چی می‌ترسی؟",
        "باشه، عجله نکن. من گوش می‌کنم."
    ],
    "followup": [
        "می‌خوای یه کم بیشتر بازش کنی؟",
        "این برات چه معنایی داره؟",
        "الان چه چیزی سخت‌تره؟"
    ],
    "default": [
        "من گوش می‌کنم… ادامه بده.",
        "می‌خوای بیشتر توضیح بدی؟",
        "اینجا امنه، هرچی هست بگو."
    ]
}

# ===== توابع =====
def detect_mood(text):
    text = text.lower()
    for mood, keywords in MOODS.items():
        if any(k in text for k in keywords):
            return mood
    return None

def get_user(user_id):
    if user_id not in user_state:
        user_state[user_id] = {
            "last_mood": None,
            "last_seen": time.time(),
            "turns": 0
        }
    return user_state[user_id]

# ===== هندلرها =====
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, WELCOME_TEXT)

@bot.message_handler(func=lambda message: True)
def reply(message):
    user_id = message.from_user.id
    text = message.text
    user = get_user(user_id)
    user["turns"] += 1

    mood = detect_mood(text)

    # اگر احساس جدید تشخیص داده شد
    if mood:
        user["last_mood"] = mood
        answer = random.choice(RESPONSES[mood])

    # اگر قبلاً احساس داشته و مکالمه ادامه داره
    elif user["last_mood"] and user["turns"] > 1:
        answer = random.choice(RESPONSES["followup"])

    # حالت پیش‌فرض
    else:
        answer = random.choice(RESPONSES["default"])

    bot.send_message(message.chat.id, answer)

print("LUNO (advanced rule-based) is running...")
bot.infinity_polling()
