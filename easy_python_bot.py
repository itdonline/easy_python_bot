#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Telegram bot that works like Python interpreter

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

from subprocess import Popen, PIPE

import time


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

chat_proc_dict = {}

def start(bot, update):
    with open('hello_message.txt', 'r') as hello_message_file:
        bot.sendMessage(update.message.chat_id, text=hello_message_file.read())


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    logger.info('User %s sent message: %s' % (update.message.from_user, update.message.text))
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def text_message_handler(bot, update):
    print chat_proc_dict

    chat_id = update.message.chat_id
    message = update.message.text

    logger.info('User %s (%s) sent message: %s' % (update.message.from_user, chat_id, message))

    if chat_id not in chat_proc_dict:
        proc = Popen('python -i',
                     shell=True,
                     stdin=PIPE, stdout=PIPE, stderr=PIPE)

        chat_proc_dict[chat_id] = {'proc': proc,
                                   'bot': bot,
                                   'timestamp': time.time()}

    chat_proc_dict[chat_id]['proc'].stdin.write(message + '\n')

    # bot.sendMessage(chat_id, text=chat_proc_dict[chat_id]['proc'].stdout.readline())


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():

    # Read secret token from file
    with open('easy_python_bot_token', 'r') as easy_python_bot_token_file:
        easy_python_bot_token = easy_python_bot_token_file.readline()

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(easy_python_bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], text_message_handler))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()