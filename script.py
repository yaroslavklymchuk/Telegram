#!/usr/bin/env python

from telegram.ext import Updater
from telegram.ext import CommandHandler
import random


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello!")


def add_word(bot, update, args):
    file = open('vocabulary.txt', 'r')
    lines = [el.strip() for el in file.readlines()]
    file.close()
    t = 0
    with open('vocabulary.txt', 'a') as file:
        for el in args:
            if el not in lines:
                file.write(el)
                file.write('\n')
                t += 1
            else:
                bot.send_message(chat_id=update.message.chat_id, text='"%s" has already exist in a vocabulary' % el)

    file.close()

    bot.send_message(chat_id=update.message.chat_id, text='Added %d new words' % t)


def delete_word(bot, update, args):
    file = open('vocabulary.txt', 'r')
    lines = [el.strip() for el in file.readlines()]
    file.close()

    for el in args:
        if (el in lines):
            lines.remove(el)
            bot.send_message(chat_id=update.message.chat_id, text='"%s" removed from vocabulary' % el)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='"%s" not in a vocabulary' % el)

    with open('vocabulary.txt', 'w') as file:
        for el in lines:
            file.write(el)
            file.write('\n')

    file.close()


def repeat_word(bot, update):
    file = open('vocabulary.txt', 'r')
    lines = [el.strip() for el in file.readlines()]
    file.close()

    if (len(lines) != 0):
        text_to_response = lambda: random.choice(lines)
        bot.send_message(chat_id=update.message.chat_id, text=text_to_response())

    else:
        bot.send_message(chat_id=update.message.chat_id, text='Empty vocabulary')


TOKEN = '578051456:AAHv57HpGkfDXEj1QZYf2VB2dPj5CEQQexc'
updater = Updater(token=TOKEN)

start_handler = CommandHandler('start', start)
updater.dispatcher.add_handler(start_handler)

add_word_handler = CommandHandler('a', add_word, pass_args=True)
updater.dispatcher.add_handler(add_word_handler)

repeat_word_handler = CommandHandler('r', repeat_word)
updater.dispatcher.add_handler(repeat_word_handler)

delete_word_handler = CommandHandler('d', delete_word, pass_args=True)
updater.dispatcher.add_handler(delete_word_handler)

updater.start_polling()