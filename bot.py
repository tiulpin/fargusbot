import os
import requests
import logging
from uuid import uuid4

from telegram import Audio, Voice, InlineQueryResultAudio, ParseMode, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)

# Get a new dictionary on every launch
file = open("dict.csv","r")
data = {}
for line in file:
  item = line.split(',')
  data[f'mp3/{item[0]}.mp3'] = item[1]


def get_audio(query):
  path = next((filename for filename, text in data.items() if text.startswith(query)), None)
  if not path:
    path = 'mp3/INTRO4.mp3'
  return path

# Define a few command handlers
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def start(update, context):
    update.message.reply_text('черт фил ты пьешь эту гадость тебе не надо было это пить')


def help(update, context):
    update.message.reply_text("""
    ...
    """)


def transform_answer(result):
    return InlineQueryResultAudio(
      id=str(uuid4()),
      audio_url=result['audio'],
      title=result['text']
    )


def inlinequery(update, context):
    query = update.inline_query.query
    audio_url = get_audio(query)
    result = {'text': query, 'audio': audio_url}
    results = map(transform_answer, result)
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

