def add_number(add_one, add_two):
    print(add_one + add_two)


def subtract_number(subtract_one, subtract_two):
    print(subtract_one - subtract_two)


def multiply_number(multiply_one, multiply_two):
    print(multiply_one * multiply_two)


def divide_number(divide_one, divide_two):
    print(divide_one / divide_two)


def create_fraction(fraction_name, fraction_amount, fraction_shape, fraction_highlighted, fraction_data, is_printed):
    if fraction_name == "":
        print("ERROR: NAME CANNOT BE EMPTY")

    if fraction_amount == 0:
        print("ERROR: AMOUNT CANNOT BE EMPTY")

    if fraction_amount == 1:
        print("ERROR: AMOUNT CANNOT BE BELOW 2")

    if fraction_shape == "":
        print("ERROR: SHAPE CANNOT BE EMPTY")

    if fraction_highlighted == 0:
        print("ERROR: HIGHLIGHT CANNOT BE EMPTY")

    if fraction_data == "":
        print("ERROR: DATA CANNOT BE EMPTY.")

    if is_printed:
        print(fraction_name)
        print("--------------")
        print("(" + fraction_shape + ")")
        print("---------------------")
        print(fraction_amount)
        print("-")
        print(fraction_highlighted)

