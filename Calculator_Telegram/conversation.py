from config import TOKEN
from bot import (RECALCULATE, WAY, ENTER_COMPLEX, ENTER_FLOAT, OPERATION,
                choose_path_to_work, get_complex_number, get_float_number,
                get_operation, start, cancel)
            

from telegram import Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from telegram.ext import Updater, CommandHandler

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler( # здесь строится логика разговора
    # точка входа в разговор
    entry_points=[CommandHandler('start', start)],
    # этапы разговора, каждый со своим списком обработчиков сообщений
    states={
        WAY: [MessageHandler(Filters.regex('^(Rational|Complex)$'), choose_path_to_work)],
        ENTER_FLOAT: [MessageHandler(Filters.text & ~Filters.command, get_float_number)],
        ENTER_COMPLEX: [MessageHandler(Filters.text & ~Filters.command, get_complex_number)],
        OPERATION: [MessageHandler(Filters.text & ~Filters.command, get_operation)],
        RECALCULATE: [CommandHandler('start', start)],
    },
    # точка выхода из разговора
    fallbacks=[CommandHandler('cancel', cancel)],
    
)

# Добавляем обработчик разговоров `conv_handler`
dispatcher.add_handler(conv_handler)

# Запуск бота
print('Server started')
updater.start_polling()
updater.idle()