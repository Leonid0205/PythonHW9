def operations_num1_num2(oper, a, b):
    '''Makes a calculation that depends on operation and two operands was given'''
    if oper == '+':
        return a + b
    elif oper == '-':
        return a - b
    elif oper == '/':
        return a / b
    elif oper == '*':
        return a * b
    else:
        return 'Incorrect operation'