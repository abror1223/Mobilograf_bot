import telebot
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = "8304478351:AAFyt4ESWpJgyq2qY-Bqnb2ra07DJ41tuEo"
ADMIN_ID = 1010237111

bot = telebot.TeleBot(TOKEN)

questions = [
    "1. Ismingiz va familiyangiz:",
    "2. Yoshingiz:",
    "3. Yashash joyingiz (faqat Shurchi hududi):",
    "4. Telefon raqamingiz:",
    "5. Hozir nima bilan bandsiz?",
    "6. Bu sohada qancha vaqt yurishni o'ylayapsiz (qiziqishingiz)?",
    "7. Ilgari qilgan videolaringiz bormi? (Agar bor bo‘lsa, link yoki qisqacha yozing):",
    "8. Iltimos, o'zingizning rasmingizni yuboring (faqat siz ko‘rasiz, boshqa joyda ishlatilmaydi)."
]

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'answers': []}
    bot.send_message(chat_id, "📋 Assalomu alaykum!\n\nMobilograf shogird bo'lish uchun quyidagi savollarga javob bering.")
    bot.send_message(chat_id, questions[0])

@bot.message_handler(content_types=['text', 'photo'])
def handle_response(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        return

    current_index = len(user_data[chat_id]['answers'])

    if current_index == len(questions) - 1 and message.content_type != 'photo':
        bot.send_message(chat_id, "📷 Iltimos, faqat rasmingizni yuboring.")
        return

    if message.content_type == 'text':
        user_data[chat_id]['answers'].append(message.text)
        if current_index + 1 < len(questions) - 1:
            bot.send_message(chat_id, questions[current_index + 1])
        elif current_index + 1 == len(questions) - 1:
            bot.send_message(chat_id, questions[-1])

    elif message.content_type == 'photo':
        user_data[chat_id]['photo'] = message.photo[-1].file_id
        summary = "\n".join(f"{questions[i]} {user_data[chat_id]['answers'][i]}" for i in range(len(user_data[chat_id]['answers'])))
        caption = f"📥 Yangi shogird arizasi:\n\n{summary}"
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption)
        bot.send_message(chat_id, "✅ Arizangiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog'lanamiz.")
        del user_data[chat_id]

bot.polling()
