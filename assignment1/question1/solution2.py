def luhn_algorithm(card_number):
    digits = [int(digit) for digit in card_number if digit.isdigit()]
    checksum = sum(digits[::2] + [sum(divmod(d * 2, 10)) for d in digits[-2::2]])
    return checksum % 10 == 0


def validate_credit_card(card_number):
    if luhn_algorithm(card_number):
        return "Valid Credit Card Number"
    else:
        return "Invalid Credit Card Number"


# Example usage
credit_card_number = input("Enter your credit card number: ")
result = validate_credit_card(credit_card_number)
print(result)
