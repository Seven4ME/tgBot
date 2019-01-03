import telebot
from telebot import types
import sqlite3

conn = sqlite3.connect('about_costumer.db', check_same_thread=False)

c = conn.cursor()


bot = telebot.TeleBot('548904581:AAFb8SOsHYRls-hZUS8YMkI0uW570ZeuVL8')

@bot.message_handler(commands=['start', 'help', 'url'])
def welcome_message(message):
    markup = types.InlineKeyboardMarkup()
    ua_btn = types.InlineKeyboardButton(text='🇺🇦 Украинский', callback_data='ua')
    ru_btn = types.InlineKeyboardButton(text='🇷🇺 Русский', callback_data='ru')
    markup.add(ua_btn, ru_btn)
    bot.reply_to(message, 'Привет, {}.\n На каком языке вам будет удобно общаться?'.format(message.from_user.first_name), reply_markup=markup)

    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_id = message.from_user.id
    username = message.from_user.username

    #c.execute('''INSERT INTO about_costumer(first, last, username, id)
    #              VALUES(?,?,?,?)''', (first_name,last_name, user_id, username))
    #c.execute('SELECT * FROM about_costumer')
    #print(c.fetchall())

    #conn.commit()


@bot.callback_query_handler(func=lambda call: True)
def which_language(call):
    if call.message:
        if call.data == 'ua':
            markup = types.InlineKeyboardMarkup()
            faq_ua = types.InlineKeyboardButton(text='⁉️Частi питання️', callback_data='faq_ua')
            primary_req_ua = types.InlineKeyboardButton(text='⚠️Основнi вимоги', callback_data='primary_req_ua')
            call_operator_ua = types.InlineKeyboardButton(text='📲Дзвiнок оператору',
                                                          url='https://alexcredit.ua/pages/contact/uk')
            how_to_get_ua = types.InlineKeyboardButton(text='💸Як отримати грошi?', callback_data='how_to_get_ua')
            markup.add(faq_ua, primary_req_ua, call_operator_ua, how_to_get_ua)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ви обрали 🇺🇦(UA) мову \n Оберiть варiант, який вас цiкавить: ",reply_markup=markup)






        elif call.data == 'ru':
            markup = types.InlineKeyboardMarkup()
            faq_ru = types.InlineKeyboardButton(text='⁉️Частые вопросы', callback_data='faq_ru')
            primary_req_ru = types.InlineKeyboardButton(text='⚠️Основные требования', callback_data='primary_req_ru')
            call_operator_ru = types.InlineKeyboardButton(text='📲Звонок Оператору',
                                                          url='https://alexcredit.ua/pages/contact')
            how_to_get_ru = types.InlineKeyboardButton(text='💸Как получить деньги?', callback_data='how_to_get_ru')
            markup.add(faq_ru, primary_req_ru, call_operator_ru, how_to_get_ru)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали 🇷🇺(RU) язык", reply_markup=markup)

if __name__=='__main__':
    bot.polling(none_stop=True)