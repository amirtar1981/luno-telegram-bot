import telebot

BOT_TOKEN = "8510729176:AAHMfQdZPc3F8u4wzNzusEev9B-ma9vBA40"
bot = telebot.TeleBot(BOT_TOKEN)

WELCOME_TEXT = (
    "من لونو هستم 🌙\n"
    "یه جای آروم برای حرف زدن.\n\n"
    "هر چی تو دلت هست بنویس."
)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, WELCOME_TEXT)

@bot.message_handler(func=lambda message: True)
def reply(message):
    text = message.text.lower()

    if any(word in text for word in ["sad", "upset", "depressed", "غمگین", "ناراحتم"]):
        answer = "می‌فهمم… اگه دوست داری بیشترش رو بگو، من گوش می‌کنم."
    elif any(word in text for word in ["angry", "mad", "عصبانی"]):
        answer = "به نظر میاد خیلی تحت فشاری. چی بیشتر اذیتت کرده؟"
    elif any(word in text for word in ["hi", "hello", "سلام"]):
        answer = "سلام، خوش اومدی 🌱"
    else:
        answer = "من اینجام. ادامه بده…"

    bot.send_message(message.chat.id, answer)

print("LUNO is running...")
bot.infinity_polling()
