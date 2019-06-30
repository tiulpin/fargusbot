import os
import requests
import logging
from uuid import uuid4

from telegram import InlineQueryResultVoice, ParseMode, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)

# Get a new dictionary on every launch
file = open("dict.csv","r")
next(file)
data = {}
for line in file:
  item = line.split(',')
  data[item[0]] = item[1]


def get_audio_names(query):
  result = list(filter(lambda key: data[key].find(query) != -1, data.keys()))[:10]
  return result, [data[key][:-1] for key in result]

# Define a few command handlers
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def start(update, context):
    update.message.reply_text('черт фил ты пьешь эту гадость тебе не надо было это пить')


def help(update, context):
    update.message.reply_text("""
    ...
    """)


def inlinequery(update, context):
    query = update.inline_query.query
    audio_names, titles = get_audio_names(query)

    results = [
      InlineQueryResultVoice(id=str(uuid4()),
        voice_url=f'https://raw.githubusercontent.com/tiulpin/tg-fargusbot/master/mp3/{audio_name}.mp3',
        title=title) for audio_name, title in zip(*get_audio_names(query))]

    update.inline_query.answer(results)


def main():
    updater = Updater(os.environ['TELEGRAM_TOKEN'], use_context=True)
    dp = updater.dispatcher

    dp.add_error_handler(error)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(InlineQueryHandler(inlinequery))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

