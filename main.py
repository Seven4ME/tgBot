import telebot
from telebot import types
import psycopg2
from flask import Flask, request
import os

conn = psycopg2.connect(dbname='d1rdnj891jf6jg', user='gcnaoqmstjxbtn',
                        password='7d8d6df9df2dda63e93feb0ef321a0397673d6eaf45c0c54b1ef079613a21493', host='ec2-46-137-84-173.eu-west-1.compute.amazonaws.com')
server = Flask(__name__)
c = conn.cursor()
bot_id = '1215880984:AAHuLxPx8vEuOVPIznPhOWBCKkBFUlZbKgs'
bot = telebot.TeleBot(bot_id)

@bot.message_handler(commands=['start', 'help', 'url'])
def welcome_message(message):
    markup = types.InlineKeyboardMarkup()
    how_to_get_ua = types.InlineKeyboardButton(text='💸Получить Бонус',
                                               url='https://l1l.pw/3d79k3/sub1:sub2:sub3:sub4:sub5',
                                               callback_data='how_to_get_ua')

    if how_to_get_ua.callback_data == 'how_to_get_ua':
        pass

    markup.add(how_to_get_ua)
    img = open('images/photo_2020-08-21_21-08-26.jpg', 'rb')
    bot.send_photo(chat_id=message.from_user.id, photo=img)
    bot.send_message(chat_id=message.from_user.id,
                     text="Забирай космические бонусы, {}. Нажимай на кнопку под сообщением и крути колесо. Тебя ждут до 5️⃣0️⃣0️⃣ FS + 5️⃣ 0️⃣0️⃣0️⃣ гривен к первому депозиту. Предложение актуально только 48 часов. Не тяни👇".format(message.from_user.first_name),
                     reply_markup=markup)

    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        query_string = """INSERT INTO user_data_telegram_bot(first_name, last_name, user_id, username) VALUES (%s,%s,%s,%s)"""
        c.execute(query_string, (first_name, last_name, user_id, username))

        conn.commit()
    except:
        print('duplicated')




if __name__ == '__main__':
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
    bot.polling(none_stop=True)
