import os
import telebot
import google.generativeai as genai
from telebot import types

# Отримуємо токени з налаштувань (Settings -> Variables and Secrets)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """Ти — вчитель німецької мови A1. 
Відповідай чітко: 1. Переклад. 2. Речення з ЖИРНИМ словом. 3. Переклад речення."""

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("✍️ Скласти речення", "✅ Виправити помилку")
    bot.send_message(message.chat.id, "Hallo! Я готовий допомагати з німецькою.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nЗапит: {message.text}")
        bot.reply_to(message, response.text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, "Ой, виникла помилка. Спробуйте пізніше.")

# Запуск з ігноруванням помилок мережі (щоб бот не падав)
if __name__ == "__main__":
    print("Бот запускається...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
