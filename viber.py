from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.keyboard_message import KeyboardMessage
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.rich_media_message import RichMediaMessage
from viberbot.api.messages.picture_message import PictureMessage

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
import json
import time
import logging
import sched
import threading
import os
import locale

app = Flask(__name__)

viber = Api(BotConfiguration(
    name='Kosmolot',
    avatar='',
    auth_token='4c0b26f3c8a7d3df-d671ca5492ec4e71-48a92da09ff86295'
))


webhook_url = 'https://kosmolot-bot.herokuapp.com/viber'

@app.route('/viber', methods=['POST'])
def incoming():
    print("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())
    viber2_request = viber.parse_request(request.get_data().decode('utf-8'))
    #viber.post_messages_to_public_account(sender=viber_request.get_sender().get_id(),
                                          #messages=[TextMessage(text="sample message")])

    if isinstance(viber2_request, ViberConversationStartedRequest):
        SAMPLE_BUTTON = {
            "Type": "keyboard",
            "InputFieldState": "hidden",
            "Buttons": [

                {
                    "Columns": 3,
                    "Rows": 1,
                    "ActionBody": "_bot_product",
                    "Text": '<font color="#f5f8f6"><b>Продукция</b></font>',
                    "Silent": "true",
                    "BgColor": "#015b29",
                    "TextSize": "large",
                    "TextHAlign": "center",
                    "TextVAlign": "middle",
                    "ActionType": "reply",

                    # "ImageScaleType":"fit"
                    # "BgMediaType": "picture",
                    # "ImageScaleType": "fit",
                    # "BgMediaScaleType": "fit",
                },

                {
                    "Columns": 3,
                    "Rows": 1,
                    "ActionBody": "_bot_search",
                    "Text": '<font color="#f5f8f6"><b>Поиск</b></font>',
                    "BgColor": "#015b29",
                    "TextSize": "large",
                    "TextHAlign": "center",
                    "TextVAlign": "middle",
                    "ActionType": "reply",


                }
            ]
        }

        SAMPLE_RICH_MEDIA = {
            "Type": "rich_media",
            "ButtonsGroupRows":3,
            "Buttons": [
                {
                    "Columns": 6,
                    "Rows": 2,
                    "BgMedia": "https://i.imgur.com/G5rI7pK.png",
                    "BgMediaType": "picture",
                    "BgLoop": "true",
                    "ActionType": None,
                    "Silent": "true",
                    "ActionBody": "",
                    "Image": "#",
                    "TextVAlign": "middle",
                    "TextHAlign": "center",
                    "Text": "",
                    "TextOpacity": 100,
                    "TextSize": "regular"
                },
                {
                    "Columns": 6,
                    "Rows": 1,
                    "BgColor": "#8074d6",
                    "BgMediaType": "gif",
                    "BgMedia": "#",
                    "BgLoop": "true",
                    "ActionType": None,
                    "Silent": "true",
                    "ActionBody": " ",
                    "Image": "#",
                    "TextVAlign": "middle",
                    "TextHAlign": "center",
                    "Text": "<b>Подписаться</b>",
                    "TextOpacity": 100,
                    "TextSize": "regular"
                }
            ],




        }

        SAMPLE_ALT_TEXT = "Забирай бонус!"

        message = RichMediaMessage(rich_media=SAMPLE_RICH_MEDIA, alt_text=SAMPLE_ALT_TEXT, min_api_version=2) #json.loads?

        viber.send_messages(viber2_request.user.id, [message])

    RICH_MEDIA_BUTTON = {
        "Type": "rich_media",
        "ButtonsGroupRows": 1,
        "Buttons": [
            {
                "Columns": 6,
                "Rows": 1,
                "BgColor": "#8074d6",
                "BgMediaType": "gif",
                "BgMedia": "#",
                "BgLoop": "true",
                "ActionType": 'open-url',
                "Silent": "true",
                "ActionBody": "http://hotto.top/cosmo",
                "Image": "#",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                "Text": "<b>Забрать бонус🎁</b>",
                "TextOpacity": 100,
                "TextSize": "regular"
            }
        ],

    }
    RICH_MEDIA_ALT = "Забирай бонус!"
    if isinstance(viber2_request, ViberMessageRequest):
        viber.send_messages(viber2_request.sender.id, [
            PictureMessage(media='https://i.imgur.com/wZxWrlb.jpg'),
            TextMessage(text='Забирай космические бонусы.\nНажимай на кнопку под сообщением и крути колесо. Тебя ждут до 5️⃣0️⃣0️⃣ FS + 5️⃣ 0️⃣0️⃣0️⃣ гривен к первому депозиту. \nПредложение актуально только 48 часов. Не тяни👇'),
            RichMediaMessage(rich_media=RICH_MEDIA_BUTTON, alt_text=RICH_MEDIA_ALT, min_api_version=2)
        ])



    #if isinstance(viber2_request, ViberSubscribedRequest):



            #TextMessage(text="Добрый день!\n Для начала работы с ботом наберите Начать."),
            #KeyboardMessage(keyboard=SAMPLE_BUTTON, min_api_version=6)

    if isinstance(viber_request, ViberFailedRequest):
        print("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)

def create_webhook(viber, webhook_url):
    print('hello')
    viber.set_webhook(webhook_url)

if __name__ == '__main__':
    viber.set_webhook("")
    time.sleep(1)
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, create_webhook, (viber, webhook_url,))
    t = threading.Thread(target=scheduler.run)
    app.run(debug=True)
