import re


def validate_credit_card(card_number):
    # Define the regex pattern for a valid credit card number
    # Starts with a digit 4, 5, or 6.
    # Followed by three digits.
    # Optionally followed by hyphen.
    # Followed by four digits.
    # Optionally followed by hyphen.
    # Followed by four digits.
    # Optionally followed by hyphen.
    # Ends with four digits.
    pattern = re.compile(r'^[4-6]\d{3}[-]?\d{4}[-]?\d{4}[-]?\d{4}$')

    # Remove dashes and spaces from the card number
    card_number = re.sub(r'[-\s]', '', card_number)

    # Check if the card number matches the pattern
    if pattern.match(card_number):
        return "Valid Credit Card Number"
    else:
        return "Invalid Credit Card Number"


# Example usage
credit_card_number = input("Enter your credit card number: ")
result = validate_credit_card(credit_card_number)
print(result)
