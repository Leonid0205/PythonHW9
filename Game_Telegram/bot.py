import logging
import check
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
PLAYER = 'Player'
BOT = 'Bot'
WAY, ENTER_NAME, ENTER_NAMEPLAYER_VS_BOT, FIRST_TURN, TURN_LIMIT, TOTAL_AMOUNT, GAME1, GAME2, GAME_PLAYER_VS_BOT, RESTART = range(10)

# функция обратного вызова точки входа в разговор
def start(update, _):
    # Список кнопок для ответа
    reply_keyboard = [[PLAYER, BOT]]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Telegram "Candy game" greets you)\n'
        'Who do you want to play with?',
        reply_markup=markup_key,)
    return WAY

def choose_path_to_work(update, _):
    '''Makes a way to PLAER_VS_PLAYER or BOT_VS_PLAYER by clicking in telegram.'''
    way = update.message.text
    if way == PLAYER:
        update.message.reply_text('You choose PLAYER vs PLAER mode')
        update.message.reply_text('Input first PLAYER name: ')
        return ENTER_NAME
    elif way == BOT:
        update.message.reply_text('You choose PLAYER vs BOT mode')
        update.message.reply_text('Input PLAYER name: ')
        return ENTER_NAMEPLAYER_VS_BOT
    update.message.reply_text('You choose unexisting mode!')

def get_names_players(update, context):
    '''Function gives names to the players (if it is PLAER_VS_PLAYER mode) and redirects to next step FIRST_TURN.'''
    name = update.message.text
    if not check.check_name(update, name):
        return ENTER_NAME
    update.message.reply_text(f'You inputed PLAYER name: {name}')
    which = 'name1' if 'name1' not in context.user_data else 'name2'
    context.user_data[which] = str(name)
    if 'name2' not in context.user_data:
        update.message.reply_text('Input second PLAYER name: ')
        return ENTER_NAME
    if context.user_data['name1'] == context.user_data['name2']:
        update.message.reply_text('PLAYERS names have to be defferent)\n'
                              'Try again)')
        return ENTER_NAME
    update.message.reply_text('The lady luck will deside whose turn is first)\n'
                              'Type a number between 1 and 9)')
    return FIRST_TURN

def get_name_player_vs_bot(update, context):
    '''Function gives name to the player (if it is BOT_VS_PLAYER mode) and redirects to next step FIRST_TURN.'''
    name = update.message.text
    if not check.check_name(update, name):
        return ENTER_NAMEPLAYER_VS_BOT
    update.message.reply_text(f'You inputed PLAYER name: {name}')
    context.user_data['name1'] = str(name)
    context.user_data['name3'] = str(name)
    if 'name2' not in context.user_data:
        context.user_data['name2'] = 'Bot'
    update.message.reply_text('The lady luck will deside whose turn is first)\n'
                              'Type a number between 1 and 9)')
    return FIRST_TURN

def get_first_turn(update, context):
    '''Function determines who will take the first turn and redirects to next step TURN_LIMIT.'''
    flip = update.message.text
    if int(flip) % 2 == 0:
        if not check.luck(update, flip):
            return FIRST_TURN
        update.message.reply_text(f'It is {context.user_data["name1"]} turn!')
    else:                                       
        name2 = context.user_data['name2']
        name1 = context.user_data['name1']
        context.user_data['name1'] = name2
        context.user_data['name2'] = name1
        update.message.reply_text(f'It is {context.user_data["name1"]} turn!')
    update.message.reply_text('Input the limit of candies for player per turn: ')
    return TURN_LIMIT

def get_turn_limit(update, context):
    '''Function determines turn limit of candies and redirects to next step TOTAL_AMOUNT.'''
    turn_limit = update.message.text
    if not check.check_limit(update, turn_limit):
        return TURN_LIMIT
    update.message.reply_text(f'The limit of candies for player per turn: {turn_limit}')
    context.user_data['turn_limit'] = int(turn_limit)
    update.message.reply_text('Input the total amount of candies: ')
    return TOTAL_AMOUNT

def get_total_amount(update, context):
    '''Function determines total amount of candies. Depends on the current mode of the game redirects to next step GAME_PLAYER_VS_BOT
    (also on the matter of whose turn is first. If it is Bot turn makes it and than redirects to next step GAME_PLAYER_VS_BOT or if
    it is Player turn redirects(without making a turn) to next step GAME_PLAYER_VS_BOT) or GAME1.'''
    total_amount = update.message.text
    if not check.check_total_amount(update, total_amount, context.user_data['turn_limit']):
        return TOTAL_AMOUNT
    update.message.reply_text(f'The total amount of candies: {total_amount}')
    context.user_data['total_amount'] = int(total_amount)
    total_amount = context.user_data['total_amount']
    turn_limit = context.user_data['turn_limit']
    if context.user_data['name1'] == 'Bot':
        update.message.reply_text(f'Bot takes his move)')
        if total_amount <= turn_limit:
            turn_bot = total_amount
        else:
            turn_bot = total_amount - (turn_limit + 1) * (total_amount // (turn_limit + 1))
        total_amount -= turn_bot
        context.user_data['total_amount'] = total_amount
        update.message.reply_text(f'Bot takes {turn_bot}\n'
                                  f'The {total_amount} of candies left.\n'
                                  f"{context.user_data['name2']} how many candies will you take:")
        return GAME_PLAYER_VS_BOT
    elif context.user_data['name2'] == 'Bot':
        update.message.reply_text(f'{context.user_data["name1"]} choose a number between 1 and {context.user_data["turn_limit"]}: ')
        return GAME_PLAYER_VS_BOT
    else: 
        update.message.reply_text(f'{context.user_data["name1"]} choose a number between 1 and {context.user_data["turn_limit"]}: ')
        return GAME1

def game_start1(update, context):
    '''Function is in charge of making a turn.'''
    total_amount = context.user_data['total_amount']
    turn_limit = context.user_data['turn_limit']
    player1 = context.user_data["name1"]
    player2 = context.user_data["name2"]
    try:
        turn = int(update.message.text)
        if turn > turn_limit:
            update.message.reply_text(f'The number of candies must be between 1 and {turn_limit}.')
            return GAME1
        if turn < 1:
            update.message.reply_text(f'The number of candies must be more than Zero.')
            return GAME1
    except ValueError:
        update.message.reply_text('Invalid input!\n'
                                  'Numbers only!\n'
                                  'Try again)')
        return GAME1
    if total_amount - turn <= 0:
        update.message.reply_text(f'{player1} You won!')
        context.user_data.clear()
        reply_keyboard = [[PLAYER, BOT]]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
        'I congratulate you on your success)\n'
        'Who do you want to do?\n'
        'If you want to exit type or press: /cancel',
        reply_markup=markup_key,)
        return WAY
    total_amount -= turn
    context.user_data['total_amount'] = total_amount
    update.message.reply_text(f'{player1} took {turn}')
    update.message.reply_text(f'The {total_amount} of candies left you can take {turn_limit}.\n'
                               f'{player2} how many candies you will take.')
    return GAME2

def game_start2(update, context):
    '''Function is in charge of making a turn.'''
    total_amount = context.user_data['total_amount']
    turn_limit = context.user_data['turn_limit']
    player1 = context.user_data["name1"]
    player2 = context.user_data["name2"]
    try:
        turn = int(update.message.text)
        if turn > turn_limit:
            update.message.reply_text(f'The number of candies must be between 1 and {turn_limit}.')
            return GAME2
        if turn < 1:
            update.message.reply_text(f'The number of candies must be more than zero.')
            return GAME2
    except ValueError:
        update.message.reply_text('Invalid input!\n'
                                  'Numbers only!\n'
                                  'Try again)')
        return GAME2
    if total_amount - turn <= 0:
        update.message.reply_text(f'{player2} You won!')
        context.user_data.clear()
        reply_keyboard = [[PLAYER, BOT]]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
        'I congratulate you on your success)\n'
        'Who do you want to do?\n'
        'If you want to exit type or press: /cancel',
        reply_markup=markup_key,)
        return WAY
    total_amount -= turn
    context.user_data['total_amount'] = total_amount
    update.message.reply_text(f'{player2} took {turn}')
    update.message.reply_text(f'The {total_amount} of candies left you can take {turn_limit}.\n'
                               f'{player1} how many candies you will take.')
    return GAME1
        
def game_player_vs_bot(update, context):
    '''Function is in charge of making turns for the PLAYER_VS_BOT mode.'''
    total_amount = context.user_data['total_amount']
    turn_limit = context.user_data['turn_limit']
    player = context.user_data['name3']
    try:
        turn = int(update.message.text)
        if turn > turn_limit:
            update.message.reply_text(f'The number of candies must be between 1 and {turn_limit}.')
            return GAME_PLAYER_VS_BOT
        if turn < 1:
            update.message.reply_text(f'The number of candies must be more than zero.')
            return GAME_PLAYER_VS_BOT
    except ValueError:
        update.message.reply_text('Invalid input!\n'
                                  'Numbers only!\n'
                                  'Try again)')
        return GAME_PLAYER_VS_BOT
    total_amount -= turn
    context.user_data['total_amount'] = total_amount
    update.message.reply_text(f'{player} took {turn}')
    if total_amount <= 0:
        update.message.reply_text(f'{player} won!')
        context.user_data.clear()
        reply_keyboard = [[PLAYER, BOT]]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
        'I congratulate you on your success)\n'
        'Who do you want to do?\n'
        'If you want to exit type or press: /cancel',
        reply_markup=markup_key,)
        return WAY
    update.message.reply_text(f'The {total_amount} of candies left.')
    turn_bot = total_amount -(turn_limit + 1) * (total_amount // (turn_limit + 1))
    total_amount -= turn_bot
    context.user_data['total_amount'] = total_amount
    update.message.reply_text(f'Bot takes {turn_bot}')
    if total_amount <= 0:
        update.message.reply_text(f'Bot won!')
        context.user_data.clear()
        reply_keyboard = [[PLAYER, BOT]]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
        'I congratulate you on your success)\n'
        'Who do you want to do?\n'
        'If you want to exit type or press: /cancel',
        reply_markup=markup_key,)
        return WAY
    update.message.reply_text(f'Bot takes {turn_bot}.\n'
                              f'The {total_amount} of candies left.\n'
                              f'{player} how many candies you will take.')
    return GAME_PLAYER_VS_BOT

# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("User %s exit the game", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Goodbye my dear friend)', 
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END