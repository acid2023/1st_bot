import re
def execute_calculation(a_b_list, operator):
    try:
        if operator == '+':
            a = float(a_b_list[0])
            b = float(a_b_list[1])
            return a + b
        elif operator == '-':
            a = float(a_b_list[0])
            b = float(a_b_list[1])
            return a - b
        elif operator == '*':
            a = float(a_b_list[0])
            b = float(a_b_list[1])
            return a * b
        else:
            a = float(a_b_list[0])
            b = float(a_b_list[1])
        return a / b
    except ValueError:
        return 'valueError'
    except ZeroDivisionError:
        return 'cannot divide by zero'


def remove_first_and_last_spaces(str):
    char_list = list(str)
    i = 0
    for i in range(len(char_list)):
        if char_list[0] == ' ':
            del char_list[0]
            print(i)
        if char_list[-1] == ' ':
            del char_list[-1]
            print(i)
        i += 1
    return ''.join(char_list)


def char_check(string):
    operators_char = '*/+-'
    numbers_char = '0123456789 .'
    calc_char = operators_char + numbers_char
    #char check
    if not all(c in calc_char for c in string) or not any(c in operators_char for c in string):
        return False
    else:
        return True


def no_operator_check(string):
    operators_char = '*/+-'
    string1 = string.replace(' ', '')
    if not any(c in operators_char for c in string1):
        return False
    else:
        return True


def minus_operator_position(string):
    minus_position = string.find("-")
    if minus_position in [-1, 0]:
        return True
    return False


def wrong_operator_position(string):
    operators_char = '*/+'
    string1 = string.replace(' ', '')
    for o in operators_char:
        split_string = string1.split(o)
        if any(st == '' for st in split_string) or (any(not minus_operator_position(st) for st in split_string) and len(split_string) != 1):
            return False
    if string1[-1] == '-' or string1[1:].count('-') > 1:
        return False
    return True


def one_operator_only(string):
    operators_char = '*/+'
    i = 0
    for c in string:
        if c in operators_char:
            i += 1
    if i <= 1:
        return True
    else:
        return False


def no_spaces_between_numbers(string):
    operators_char = '*/+-'
    string1 = remove_first_and_last_spaces(string)
    i = 0
    for o in operators_char:
        check_list = string1.split(o)
        for word in check_list:
            word1 = remove_first_and_last_spaces(word)
            if word1.find(' ') != -1:
                i += 1
    if i > 3:
        return False
    return True


def two_arguements_check(string):
    operators_char = '*/+'
    if string.count('-') > 2:
        return False  #для минуса и двух аргументов может быть максимум два минуса - один как оператор и второй как знак
    for o in operators_char:
        if len(string.split(o)) > 2:  #максимум один опертаор кроме минуса = два аргумента после разбиения
            return False
    return True


def calc_arguement_check(string):
    string = remove_first_and_last_spaces(string)
    sample = r' *[-]?\d*[.]?\d* *[+/*]? *[-]?\d*[.]?\d* *'
    if re.fullmatch(sample, string) is None:
        return 'wrong arguements'
    else:
        return 'ok'


def calcus(string):
    string = remove_first_and_last_spaces(string)
    operator_choice = [o for o in "+*/" if o in string]
    if len(operator_choice) == 0:
        operator = "-"
        if string[0] != '-':  #первый аргумент не отрицательный
            string = string.split(operator)
        else:
            string = string[1:].split(operator)
            string[0] = "-" + string[0]
    else:
        operator = operator_choice[0]
        string = string.split(operator)
    return execute_calculation(string, operator)
