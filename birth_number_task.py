'''
Created on 3. 5. 2017

@author: patex1987

Generation and verification of bith numbers used in SK and CZ
'''

from sys import argv
import re
import datetime
import random


def main():
    """
    The main method of the solution

    1. if no argument is passed to the program, than it asks the user to
    insert its birth date and gender and then generates a birth number for
    based on that data
    2. if the user provides one command line parameter - then the program
    checks if the provided string is a correct birth number

    Args:

    Returns:

    Raises:

    Todo:

    Example:

    """
    if len(argv) == 1:
        generated_birth_number = generate_birth_number()
        print("\nYour birth number is: {0}".format(generated_birth_number))
        table = str.maketrans(dict.fromkeys('/'))
        remainder = int(generated_birth_number.translate(table)) % 11
        if len(generated_birth_number) == 11:
            print("Remainder after division by 11: {0}".format(remainder))
    elif len(argv) == 2:
        verif_state = verify_birth_number(argv[1])
        print(verif_state)
    elif len(argv) > 2:
        print("Wrong number of input parameters")


def generate_birth_number():
    """
    This method fires the user prompts and the birth number generator

    Args:

    Returns:
        new_number (:obj: 'str'): a generated birth number
            format: "yymmdd/cccc"

    Raises:

    Todo:

    Example:

    """
    formatted_date = date_prompt()
    gender = gender_prompt()
    if formatted_date is not None and gender is not None:
        new_number = create_number(formatted_date, gender)
    return new_number


def date_prompt():
    """
    Prompts the user until a proper birth date is provided

    Args:

    Returns:
        formatted_date (:obj: datetime.datetime): the birth date as a
            datetime object

    Raises:

    Todo:

    Example:

    """
    incorrect_format = True
    while incorrect_format:
        raw_date = input(
            "Enter Your birth date in the following format [YYYY/mm/dd]: ")
        mask = re.compile('[0-9]{4}[/][0-9]{2}[/][0-9]{2}')
        if mask.match(raw_date) is None or len(raw_date) > 10:
            print("Wrong Input Format")
            continue
        formatted_date = check_output_date(raw_date)
        if formatted_date is False:
            print("Incorrect date format")
            continue
        return formatted_date


def check_output_date(raw_date):
    """
    Checks if the input is a real date

    If the input can be converted to a datetime object
    than it can be a real date

    Args:
        raw_date (:obj: 'str'): the birth date provided by the user
            as a raw string

    Returns:
        input_date (:obj: datetime.datetime): the raw string converted to a
            datetime object
        (bool): if the conversion fails

    Raises:

    Todo:

    Example:

    """
    year = raw_date[:4]
    month = raw_date[5:7]
    day = raw_date[8:10]
    try:
        input_date = datetime.datetime(year=int(year),
                                       month=int(month),
                                       day=int(day))
        return input_date
    except:
        return False


def gender_prompt():
    """
    Prompts the user until a proper gender is provided

    the gender can be F, M, f, m

    Args:

    Returns:
        (:obj: 'str') uppercase character of the gender

    Raises:

    Todo:

    Example:

    """
    while True:
        gender = input("Enter Gender [M/F]: ")
        if gender.upper() not in ('M', 'F'):
            print("Wrong Gender")
        else:
            return gender.upper()


def create_number(formatted_date, gender):
    """
    Creates a new birth number based on the birth date and the gender

    Birth number has the following format:
    yymmdd/cccc or yymmdd/ccc
    yy - last two digits of the birth year
    mm - bith month (for females 50 is added to the value of the month)
    dd - birth day
    cccc is the control number:
        the people born before 1954 have 3 digit control number (it is actually
            the birth sequence on the given day)
        starting from 1954 a 4th digit has been added - with the addition of
            the 4th digit the whole number needs to be divisible with 11.
            if after dividing yymmddccc by 11 the remainder is 10, then the
            fourth digit is 0. I.e. the final number is not divisible by 11

    Args:

    Returns:
        (:obj: 'str') the new birth number

    Raises:

    Todo:

    Example:

    """
    month_add_val = 0
    if gender == "F":
        month_add_val = 50
    birth_number = str(formatted_date.year)[-2:] + \
        '{:02d}'.format(formatted_date.month + month_add_val) + \
        '{:02d}'.format(formatted_date.day)
    rand_part = '{:03d}'.format(random.randint(0, 100))
    const_part = int(birth_number + rand_part)
    modulo = str(const_part % 11)
    if formatted_date.year < 1954:
        return "{0}/{1}".format(birth_number, rand_part)
    if modulo == "10":
        return "{0}/{1}{2}".format(birth_number, rand_part, 0)
    return "{0}/{1}{2}".format(birth_number, rand_part, modulo)


def verify_birth_number(birth_number):
    """
    Checks if the provided birth number is in a correct format

    Args:
        (:obj: 'str') the birth number to verify

    Returns:
        (:obj: 'str') a message stating the result of the verification

    Raises:

    Todo:

    Example:

    """
    if len(birth_number) not in range(10, 12):
        return "Incorrect birth number - wrong length"
    mask = re.compile('[0-9]{6}[/][0-9]{3,4}')
    if mask.match(birth_number) is None:
        return "Incorrect format"
    input_verif_message = check_input_number_structure(birth_number)
    if input_verif_message is not None:
        return input_verif_message
    return "The given birth number is in correct format"


def check_input_number_structure(birth_number):
    """
    Checks if the provided birth number is in a correct format

    Args:
       birth_number (:obj: 'str') the birth number to verify

    Returns:
        (:obj: 'str') a message stating the result of the verification

    Raises:

    Todo:

    Example:

    """
    raw_date, code = birth_number.split('/')
    year = raw_date[:2]
    month = raw_date[2:4]
    day = raw_date[4:6]
    if int(year) >= 54 and len(birth_number) != 11:
        return "Incorrect number of digits"
    if int(month) not in list(range(1, 13)) + list(range(51, 63)):
        return "Not existing month"
    if int(day) not in range(1, 32):
        return "Not existing day"
    if int(month) in range(51, 63):
        month = str(int(month) - 50)
    try:
        datetime.datetime(year=int("19" + year),
                          month=int(month),
                          day=int(day))
    except:
        return "Impossible date"
    if len(birth_number) == 11:
        if check_sum(raw_date, code) is not None:
            return "Checksum has failed"
    return None


def check_sum(raw_date, code):
    """
    For the people born after 1954, checks if the birth number
    is divisible by 11

    Args:
        raw_date (:obj: 'str'): birth date in yymmdd format
        code (:obj: 'str'): the control number at the end of the birth number

    Returns:
        (:obj: 'str') a message stating the result of the verification

    Raises:

    Todo:

    Example:

    """
    whole_num = raw_date + code
    part_to_check = int(whole_num[:-1])
    modulo = part_to_check % 11
    if modulo == 10 and int(whole_num[-1]) != 0:
        return "Checksum has failed"
    if modulo != 10 and int(whole_num[-1]) != modulo:
        return "Checksum has failed"
    return None


if __name__ == '__main__':
    main()
