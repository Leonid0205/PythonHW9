import logging
import check
import operations

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
RAZIO = 'Rational'
COMPLEX = 'Complex'
WAY, ENTER_FLOAT, ENTER_COMPLEX, OPERATION, RECALCULATE = range(5)

# функция обратного вызова точки входа в разговор
def start(update, _):
    # Список кнопок для ответа
    reply_keyboard = [[RAZIO, COMPLEX]]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Telegram calculator greets you)'
        'Choose what numbers do you want to work with.',
        reply_markup=markup_key,)
    return WAY

def choose_path_to_work(update, _):
    '''Makes a way to RAZIO or COMPLEX numbers by clicking in telegram.'''
    way = update.message.text
    if way == RAZIO:
        update.message.reply_text('You choose RATIONAL numbers mode')
        update.message.reply_text('Input first number: ')
        return ENTER_FLOAT
    elif way == COMPLEX:
        update.message.reply_text('You choose COMPLEX numbers mode')
        update.message.reply_text('Input first number: ')
        return ENTER_COMPLEX
    update.message.reply_text('You choose unexisting mode!')

def get_float_number(update, context):
    '''Function gives rational numbers (also checks correct input) and redirects to next step OPERATION.'''
    num = update.message.text
    if not check.check_rational_number(update, num):
        return ENTER_FLOAT
    update.message.reply_text(f'You inputed a number: {num}')
    which = 'num1' if 'num1' not in context.user_data else 'num2'
    context.user_data[which] = float(num)
    if 'num2' not in context.user_data:
        update.message.reply_text('Input second number: ')
        return ENTER_FLOAT
    update.message.reply_text('Input operation "+","-", "*", "/": ')
    return OPERATION

def get_complex_number(update, context):
    '''Function gets complex numbers (also checks correct input) and redirects to next step OPERATION.'''
    num = update.message.text
    if not check.check_complex_number(update, num):
        return ENTER_COMPLEX
    update.message.reply_text(f'You inputed a number: {num}')
    which = 'num1' if 'num1' not in context.user_data else 'num2'
    context.user_data[which] = complex(num)
    if 'num2' not in context.user_data:
        update.message.reply_text('Input second number: ')
        return ENTER_COMPLEX
    update.message.reply_text('Input operation "+","-", "*", "/": ')
    return OPERATION

def get_operation(update, context):
    '''Function gets operation (also checks correct input). Depends on operation makes a calculation.
       After redirects to RECALCULATE.'''
    oper = update.message.text
    if not check.check_operation(update, oper):
        return OPERATION
    context.user_data['oper'] = oper
    num1 = context.user_data.get('num1')
    num2 = context.user_data.get('num2')
    if check.check_division(oper, num2):
        context.user_data.clear()
        update.message.reply_text('Zero Division Error(\n'
                                  'If you want to restart type or press: /start\n'
                                  'If you want to exit type or press: /cancel')
        return RECALCULATE
    expression = operations.operations_num1_num2(oper, num1, num2)
    update.message.reply_text(f'{num1} {oper} {num2} = {expression}')
    context.user_data.clear()
    update.message.reply_text('If you want to restart type or press: /start\n'
                              'If you want to exit type or press: /cancel')
    return RECALCULATE


# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("User %s exit the calculator", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Goodbye my dear friend)', 
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END