def check_operation(update, oper) -> str:
    '''Checks the operation input'''
    oper_list = ['+', '-', '*', '/']
    if oper in oper_list:
        return oper
    update.message.reply_text('Incorrect operation input. Please try again.')
def check_rational_number(update, text) -> float:
    '''Checks rational number input'''
    try:
        num = float(text)
        if num == 0 or None:
            return num == 0
        return num
    except ValueError:
        update.message.reply_text('Incorrect rational number input. Please try again.')
def check_complex_number(update, text) -> complex:
    '''Checks complex number input'''
    try:
        num = complex(text)
        if num == 0 or num == (0 + 0j) or num == (0 - 0j) or None:
            return num == 0
        return num
    except ValueError:
        update.message.reply_text('Incorrect complex number input. Please try again.')
def check_division(oper, num2) -> bool:
    '''Checks division by zero'''
    if (oper == '/' and num2 == 0) or (oper == '/' and num2 == (0 + 0j)) or (oper == '/' and num2 == (0 - 0j)):
        print('Division by zero error')
        return True
