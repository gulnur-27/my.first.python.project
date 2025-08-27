4import telebot
from telebot import types
import time
import threading
import schedule

TOKEN = ""
bot = telebot.TeleBot(TOKEN)

user_ids = set()
lesson_index = 0

english_words = [
    "🔤 Word: learn\nTranslation: учить\nExample: I want to learn English.",
    "🔤 Word: code\nTranslation: программировать\nExample: I love to code.",
    "🔤 Word: language\nTranslation: язык\nExample: English is an international language.",
    "🔤 Word: computer\nTranslation: компьютер\nExample: This is my computer.",
    "🔤 Word: keyboard\nTranslation: клавиатура\nExample: I bought a new keyboard.",
] + [f"🔤 Word {i+6}: example word" for i in range(50 - 5)]

python_lessons = [
    "🐍 Lesson: print('Hello!') – вывод текста",
    "🐍 Lesson: a = 5 – переменная с числом",
    "🐍 Lesson: if a > 3: – условие",
    "🐍 Lesson: for i in range(5): – цикл for",
    "🐍 Lesson: def greet(): – функция",
] + [f"🐍 Lesson {i+6}: example lesson" for i in range(50 - 5)]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_ids.add(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📘 Английский", "🐍 Python")
    bot.send_message(message.chat.id,
        "Привет! 👋\nЯ буду каждый день присылать тебе новое английское слово и урок по Python!",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "📘 Английский")
def send_english(message):
    bot.send_message(message.chat.id, english_words[lesson_index % len(english_words)])

@bot.message_handler(func=lambda message: message.text == "🐍 Python")
def send_python(message):
    bot.send_message(message.chat.id, python_lessons[lesson_index % len(python_lessons)])

def send_daily_lessons():
    global lesson_index
    for user_id in user_ids:
        try:
            word = english_words[lesson_index % len(english_words)]
            lesson = python_lessons[lesson_index % len(python_lessons)]
            bot.send_message(user_id, "📘 Сегодняшнее слово:\n" + word)
            bot.send_message(user_id, "🐍 Урок Python:\n" + lesson)
        except Exception as e:
            print(f"Ошибка при отправке: {e}")
    lesson_index += 1

schedule.every().day.at("09:00").do(send_daily_lessons)

def schedule_thread():
    while True:
        schedule.run_pending()
        time.sleep(30)

threading.Thread(target=schedule_thread).start()

print("✅ Бот запущен...")
bot.polling()