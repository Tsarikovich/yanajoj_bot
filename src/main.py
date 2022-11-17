import json
import telebot
import os
from config import user_message_chain, admin_message_chain, message_to_send_template, subscribe_user_message_chain
from db import collection

bot = telebot.TeleBot(os.getenv('TG_BOT_TOKEN'), parse_mode=None, threaded=False)

destination_group_id = int(os.getenv('DESTINATION_GROUP_ID'))
admin_id = int(os.getenv('ADMIN_ID'))


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    add_subscriber(message.chat.id)
    bot.send_message(message.chat.id, text=subscribe_user_message_chain[0])


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    remove_subscriber(message.chat.id)
    bot.send_message(message.chat.id, text=subscribe_user_message_chain[1])


@bot.message_handler(commands=['unsubscribe'])
def start(message):
    photo = open('0.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)

    bot.send_message(message.chat.id, text=user_message_chain[0])
    bot.send_message(message.chat.id, text=user_message_chain[1])
    bot.register_next_step_handler(message, get_name)


@bot.message_handler(commands=['start'])
def start(message):
    photo = open('0.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)

    bot.send_message(message.chat.id, text=user_message_chain[0])
    bot.send_message(message.chat.id, text=user_message_chain[1])
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    name = message.text.strip()
    photo = open('1.jpg', 'rb')
    bot.send_photo(message.from_user.id, photo)
    bot.send_message(message.from_user.id, text=user_message_chain[2].format(name=name))
    bot.register_next_step_handler(message, get_description, name.capitalize())


def get_description(message, name):
    description = message.text.lower().strip()
    bot.send_message(message.from_user.id, text=user_message_chain[3])
    bot.register_next_step_handler(message, get_contact, name, description)


def get_contact(message, name, description):
    contact = message.text.lower().strip()
    send_data(name, description, contact)
    bot.send_message(message.from_user.id, text=user_message_chain[4].format(name=name))


def send_data(name, description, contact):
    bot.send_message(destination_group_id,
                     text=user_message_chain[5].format(name=name, description=description, contact=contact))


@bot.message_handler(func=lambda message: message.from_user.id == admin_id and
                                          (message.text.strip().startswith('https://www.youtube')
                                           or message.text.strip().startswith('https://youtube')
                                           or message.text.strip().startswith('https://youtu.be')))
def send_stream_notification(message):
    link = message.text.lower().strip()

    bot.send_message(message.chat.id, text=admin_message_chain[0])
    bot.register_next_step_handler(message, get_stream_name, link)


def get_stream_name(message, link):
    stream_name = message.text.strip()
    result_message_to_send = message_to_send_template.format(name_stream=stream_name, link=link)

    bot.send_message(message.chat.id, text=admin_message_chain[1].format(user_count=get_subscribers_count()))
    subscribers = get_subscribers()

    for subscriber in subscribers:
        bot.send_message(subscriber['tg_id'], result_message_to_send)

    bot.send_message(message.chat.id, text=admin_message_chain[2])


def process_event(event):
    request_body_dict = json.loads(event['body'])
    update = telebot.types.Update.de_json(request_body_dict)
    bot.process_new_updates([update])


def get_subscribers_count():
    return collection.count_documents({})


def get_subscribers():
    return collection.find({})


def add_subscriber(user_id):
    collection.update_one({'tg_id': user_id}, {'$set': {'tg_id': user_id}}, upsert=True)


def remove_subscriber(user_id):
    collection.delete_one({'tg_id': user_id})


def main(event=None, context=None):
    process_event(event)
    return {
        'statusCode': 200
    }
