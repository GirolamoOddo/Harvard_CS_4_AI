def get_long(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a long integer.")

def is_valid(card_number):
    sum = 0
    multiply = False

    while card_number > 0:
        digit = card_number % 10
        card_number //= 10

        if multiply:
            digit *= 2
            digit = (digit % 10) + (digit // 10)

        sum += digit
        multiply = not multiply

    return sum % 10 == 0

def card_type(card_number):
    length = 0
    temp = card_number

    while temp > 0:
        temp //= 10
        length += 1

    if (length == 15) and (card_number // 10000000000000 == 34 or card_number // 10000000000000 == 37):
        return "AMEX"
    elif (length == 16) and (51 <= card_number // 100000000000000 <= 55):
        return "MASTERCARD"
    elif (length == 13 or length == 16) and (card_number // 1000000000000 == 4 or card_number // 1000000000000000 == 4):
        return "VISA"
    else:
        return "INVALID"

def main():
    card_number = 0

    while card_number <= 0:
        card_number = get_long("Number: ")

    if is_valid(card_number):
        print(card_type(card_number))
    else:
        print("INVALID")


main()
