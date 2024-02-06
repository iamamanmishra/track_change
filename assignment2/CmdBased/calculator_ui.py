from calculator import Calculator


def get_user_input():
    operation = input("Enter operation (+, -, *, /, sqrt, pow, log, sin, cos, tan): ").lower()
    if operation not in ['+', '-', '*', '/', 'sqrt', 'pow', 'log', 'sin', 'cos', 'tan']:
        print("Invalid operation. Please choose a valid operation.")
        return get_user_input()

    if operation in ['sqrt', 'sin', 'cos', 'tan']:
        num = float(input("Enter number/angle: "))
        return operation, num

    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    return operation, num1, num2


if __name__ == "__main__":
    calculator = Calculator()

    while True:
        operation, *operands = get_user_input()

        try:
            if operation == '+':
                result = calculator.add(*operands)
            elif operation == '-':
                result = calculator.subtract(*operands)
            elif operation == '*':
                result = calculator.multiply(*operands)
            elif operation == '/':
                result = calculator.divide(*operands)
            elif operation == 'sqrt':
                result = calculator.square_root(*operands)
            elif operation == 'pow':
                result = calculator.power(*operands)
            elif operation == 'log':
                result = calculator.logarithm(*operands)
            elif operation == 'sin':
                result = calculator.sin(*operands)
            elif operation == 'cos':
                result = calculator.cos(*operands)
            elif operation == 'tan':
                result = calculator.tan(*operands)
        except ValueError as e:
            print(f"Error: {e}")
        else:
            print("Result:", result)

        another_calculation = input("Do you want to perform another calculation? (yes/no): ").lower()
        if another_calculation != 'yes':
            break
