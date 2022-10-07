from config import TOKEN
from bot import (WAY, ENTER_NAME, ENTER_NAMEPLAYER_VS_BOT, FIRST_TURN, TURN_LIMIT, TOTAL_AMOUNT, GAME1, GAME2, GAME_PLAYER_VS_BOT, RESTART,
                choose_path_to_work, game_start1, game_start2, game_player_vs_bot, get_names_players, get_name_player_vs_bot, get_first_turn, get_total_amount, get_turn_limit,
                start, cancel)
            

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
        WAY: [MessageHandler(Filters.regex('^(Player|Bot)$'), choose_path_to_work)],
        ENTER_NAME: [MessageHandler(Filters.text & ~Filters.command, get_names_players)],
        ENTER_NAMEPLAYER_VS_BOT: [MessageHandler(Filters.text & ~Filters.command, get_name_player_vs_bot)],
        FIRST_TURN: [MessageHandler(Filters.text & ~Filters.command, get_first_turn)],
        TURN_LIMIT: [MessageHandler(Filters.text & ~Filters.command, get_turn_limit)],
        TOTAL_AMOUNT: [MessageHandler(Filters.text & ~Filters.command, get_total_amount)],
        GAME1: [MessageHandler(Filters.text & ~Filters.command, game_start1)],
        GAME2: [MessageHandler(Filters.text & ~Filters.command, game_start2)],
        GAME_PLAYER_VS_BOT: [MessageHandler(Filters.text & ~Filters.command, game_player_vs_bot)],
        RESTART: [CommandHandler('start', start)],
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