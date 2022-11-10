import json
import telebot
import os
from config import message_chain

bot = telebot.TeleBot(os.getenv('TG_BOT_TOKEN'), parse_mode=None, threaded=False)

chat_id = int(os.getenv('CHAT_ID'))


@bot.message_handler(commands=['start'])
def start(message):
    photo = open('0.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)

    bot.send_message(message.chat.id, text=message_chain[0])
    bot.send_message(message.chat.id, text=message_chain[1])
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    name = message.text.strip()
    photo = open('1.jpg', 'rb')
    bot.send_photo(message.from_user.id, photo)
    bot.send_message(message.from_user.id, text=message_chain[2].format(name=name))
    bot.register_next_step_handler(message, get_description, name.capitalize())


def get_description(message, name):
    description = message.text.lower().strip()
    bot.send_message(message.from_user.id, text=message_chain[3])
    bot.register_next_step_handler(message, get_contact, name, description)


def get_contact(message, name, description):
    contact = message.text.lower().strip()
    send_data(name, description, contact)
    bot.send_message(message.from_user.id, text=message_chain[4].format(name=name))


def send_data(name, description, contact):
    bot.send_message(chat_id,
                     text=f"Новое сообщение ❗\nИмя: {name.capitalize()},\nКонтакт: {contact},\nОписание проблемы: {description}")


def process_event(event):
    request_body_dict = json.loads(event['body'])
    update = telebot.types.Update.de_json(request_body_dict)
    bot.process_new_updates([update])


def main(event=None, context=None):
    process_event(event)
    return {
        'statusCode': 200
    }
