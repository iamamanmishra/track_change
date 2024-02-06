import tkinter as tk
from tkinter import ttk
import math

from calculator import Calculator


class ScientificCalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Scientific Calculator")

        self.calculator = Calculator()

        self.create_widgets()

    def create_widgets(self):
        self.result_var = tk.StringVar(value="")

        entry_frame = ttk.Frame(self.master)
        entry_frame.grid(row=0, column=0, columnspan=5)

        entry = ttk.Entry(entry_frame, textvariable=self.result_var, font=('Helvetica', 14), justify='right')
        entry.grid(row=0, column=0, sticky='news')

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('sqrt', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('pow', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('log', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3), ('sin', 4, 4),
            ('cos', 5, 0), ('tan', 5, 1), ('(', 5, 2), (')', 5, 3), ('C', 5, 4),
        ]

        for (text, row, column) in buttons:
            ttk.Button(self.master, text=text, command=lambda t=text: self.on_button_click(t)).grid(row=row, column=column)

    def on_button_click(self, button_text):
        current_input = self.result_var.get()

        if button_text == '=':
            try:
                result = self.evaluate_expression(current_input)
                self.result_var.set(result)
            except Exception as e:
                self.result_var.set("Error")
        elif button_text == 'C':
            self.result_var.set("")
        else:
            self.result_var.set(current_input + button_text)

    def evaluate_expression(self, expression):
        try:
            result = eval(expression, {"__builtins__": None}, vars(math))
            return result
        except Exception as e:
            raise ValueError("Invalid expression")
