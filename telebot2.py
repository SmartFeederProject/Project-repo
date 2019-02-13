from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
import logging
import os

token = 'Insert Your Token Here'   #insert your tlg bot token
path = '/home/batya/Desktop/Birds'
path_current = '/home/batya/Desktop/Current'

REQUEST_KWARGS={
    'proxy_url': 'socks5://phobos.public.opennetwork.cc:1090',
    'urllib3_proxy_kwargs': {
        'username': '178972342',
        'password': 'wNdBxAN5',
    }
}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    update.message.reply_text('Hi, '+ update.message.from_user.first_name + '! Welcome to the SmartFeeder Bot ;) Press /help for all of the commands!')


def help(bot, update):
    update.message.reply_text('We have a few commands here:')
    update.message.reply_text('/start - Hii!')
    update.message.reply_text('/help - Yup, here we are...')
    update.message.reply_text('/lastphoto - Send you last photo')
    update.message.reply_text('/amount - How many birds came today')
    update.message.reply_text("/current - Look what's happening there rn!")
    update.message.reply_text("/about - Just some info")


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def amount(bot, update):
    num = len([i for i in os.listdir(path) if i.endswith('.png')])
    update.message.reply_text("I've already seen "+str(num)+" birds!")

def lastphoto(bot, update):
    last = [i for i in os.listdir(path) if i.endswith('.png')]
    last_num = [j.rstrip('.png') for j in last]
    last_num = [int(j.lstrip('img')) for j in last_num] 
    last_photo = path + '/img' + str(max(last_num)) + '.png'
    photo_file = open(last_photo, 'rb')
    update.message.reply_text("Wow! Just look at this bird!")
    update.message.reply_photo(photo_file)

def current(bot, update):
    current_photo = path_current + '/img.png'
    photo_file = open(current_photo, 'rb')
    update.message.reply_text("Seems like nothing's happening there...")
    update.message.reply_photo(photo_file)

def about(bot, update):
    update.message.reply_text('Hi! More information here:')

def main():
    updater = Updater(token,request_kwargs=REQUEST_KWARGS)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("amount", amount))
    dp.add_handler(CommandHandler("lastphoto", lastphoto))
    dp.add_handler(CommandHandler("current", current))
    dp.add_handler(CommandHandler("about", about))

    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()