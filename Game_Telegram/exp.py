# def check_name():
#     try:
#         n = input("input: ")
#         if len(n) < 10:
#             return n
#         else:
#             print('n < 10')
#             pass
#     except ValueError:
#         print('Incorrect rational number input. Please try again.')
# ttt = 'player12121'
# print(check_name())

def check_name( text) -> str:
    '''Checks length of name'''
    if 0 < len(text) < 10 and text.lower() != 'bot':
        return text
    # # else: print(False)
    # elif 0 < len(text) < 10 and text != 'bot':
    #     return text
    else: print(False)
def input_name():
    while True:
        try:
            n = input("Input name: ")
            check_name(n)
            print(n)
            break
        except ValueError:
            print("OROROROROROR")
input_name()