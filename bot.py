import telebot
from telebot import types

TOKEN = "" #Here you bot Token from @DotFather 
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start']) 
def send_welcome(message):  
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("projects", callback_data="projects"))
    markup.add(types.InlineKeyboardButton("About me", callback_data="about_me"))
    markup.add(types.InlineKeyboardButton("Sourse Code", callback_data= "sourse_code"))
    markup.add(types.InlineKeyboardButton("Social test", callback_data="social_test"))

    bot.send_message(message.chat.id, "Select one button:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'about_me':
        bot.answer_callback_query(call.id, "About me:\nName: Yrashka\nAge: 16 y.0\nProgramming languages: Python, HTML, СSS (styding now) ")
    if call.data == 'sourse_code':  
        try:
            with open('bot.py', 'rb') as script_file:
                bot.send_document(
                    call.message.chat.id,  
                    document=script_file, 
                    caption="Here's your file! 📁"
                )
        except FileNotFoundError:
            bot.send_message(call.message.chat.id, "I don't see file!")
    
    bot.answer_callback_query(call.id)

    if call.data == 'social_test':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Insta", "https://www.instagram.com/yrashka200"))
        markup.add(types.InlineKeyboardButton("Bluesky", "https://bsky.app/profile/yrashka.bsky.social"))
        markup.add(types.InlineKeyboardButton("Github", "https://github.com/Yrashka2025"))

        bot.send_message(call.message.chat.id, "Here's links:", reply_markup=markup)

    if call.data == 'prujects':
        bot.answer_callback_query(call.message.chat.id, "1. https://github.com/Yrashka2025/Web-Portfolio - Web Portfolio\n2. This bot-potfolio (Sourse code in start menu buttons) ")

    

if __name__ == '__main__':
    print("🤖 Bot is runing....")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Eror: {e}")