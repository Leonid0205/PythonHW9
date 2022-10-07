def check_name(update, text) -> str:
    '''Checks length of name and RESERVED name ("Bot" and "bot")'''
    if 2 < len(text) < 10 and text.lower() != 'bot':
        return text
    update.message.reply_text('Requrement are:\n'
                              'Name length needs to be between 3 and 10 symbols.\n'
                              'Name "Bot" and "bot" are reserved.\n'
                              'Try again.')
def check_limit(update, text) -> int:
    '''Checks variable 'limit' it needs to be int also positive and above zero'''
    try:
        turn_limit = int(text)
        if turn_limit > 0:
            return turn_limit
        else:    
            update.message.reply_text('The number needs to be positive and not zero!!! ')
    except ValueError:
        update.message.reply_text('ValueError!')
def check_total_amount(update, text, turn_limit) -> int:
    '''Checks variable 'total_amount' it needs to be int also positive and above "turn_limit"'''
    try:
        total_amount = int(text)
        if total_amount > 0 and total_amount > turn_limit:
            return total_amount
        else:    
            update.message.reply_text('The number needs to be positive and more than the limit!!! ')
    except ValueError:
        update.message.reply_text('ValueError!')
def luck(update, text) -> int:
    '''Checks variable "number" it needs to be int and in range between 1 to 9'''
    try:
        number = int(text)
        if 10 > number > 0 :
            return number
        else:    
            update.message.reply_text('The number needs to be between 1 and 9!!! Try again) ')
    except ValueError:
        update.message.reply_text('ValueError!')