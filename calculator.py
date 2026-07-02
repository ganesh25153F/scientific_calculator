import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import math
from calc_utils import safe_dict, prepare_expression

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ScientificCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Scientific Calculator")
        self.geometry("420x650")
        self.resizable(False, False)
        self.configure(fg_color="#0f1115")

        self.expression = ""
        self.history = []

        self.colors = {
            "bg": "#0f1115",
            "panel": "#151922",
            "button": "#232833",
            "button_hover": "#2d3441",
            "accent": "#4aa3ff",
            "accent_hover": "#2f84e8",
            "danger": "#d9534f",
            "text": "#ffffff",
            "muted": "#b8c0cc",
        }

        self.safe_dict = safe_dict
        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        top_frame = ctk.CTkFrame(self, fg_color=self.colors["bg"])
        top_frame.pack(fill="x", padx=15, pady=(15, 5))

        title_label = ctk.CTkLabel(
            top_frame,
            text="Scientific Calculator",
            font=("Arial", 22, "bold"),
            text_color=self.colors["text"]
        )
        title_label.pack(anchor="w")

        self.display_var = tk.StringVar(value="")
        self.result_var = tk.StringVar(value="0")

        display_frame = ctk.CTkFrame(self, fg_color=self.colors["panel"], corner_radius=20)
        display_frame.pack(fill="x", padx=15, pady=10)

        self.display = ctk.CTkEntry(
            display_frame,
            textvariable=self.display_var,
            height=60,
            font=("Consolas", 24),
            fg_color=self.colors["panel"],
            text_color=self.colors["text"],
            border_width=0,
            justify="right"
        )
        self.display.pack(fill="x", padx=15, pady=(15, 5))

        self.result_label = ctk.CTkLabel(
            display_frame,
            textvariable=self.result_var,
            font=("Consolas", 18, "bold"),
            text_color=self.colors["accent"]
        )
        self.result_label.pack(anchor="e", padx=18, pady=(0, 12))

        btn_frame = ctk.CTkFrame(self, fg_color=self.colors["bg"])
        btn_frame.pack(fill="both", expand=True, padx=15, pady=10)

        buttons = [
            ["AC", "DEL", "%", "/"],
            ["sin(", "cos(", "tan(", "*"],
            ["sqrt(", "log(", "ln(", "-"],
            ["7", "8", "9", "+"],
            ["4", "5", "6", "("],
            ["1", "2", "3", ")"],
            ["0", ".", "pi", "e"],
            ["x²", "xʸ", "!", "="],
        ]

        for r, row in enumerate(buttons):
            for c, text in enumerate(row):
                self.create_button(btn_frame, text, r, c)

        history_frame = ctk.CTkFrame(self, fg_color=self.colors["bg"])
        history_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.history_label = ctk.CTkLabel(
            history_frame,
            text="History will appear here",
            font=("Arial", 12),
            text_color=self.colors["muted"]
        )
        self.history_label.pack(anchor="w")

    def create_button(self, parent, text, row, col):
        color = self.colors["button"]
        hover = self.colors["button_hover"]

        if text in ["=", "AC"]:
            color = self.colors["accent"]
            hover = self.colors["accent_hover"]

        if text == "DEL":
            color = self.colors["danger"]
            hover = "#b84a47"

        btn = ctk.CTkButton(
            parent,
            text=text,
            width=85,
            height=55,
            corner_radius=14,
            fg_color=color,
            hover_color=hover,
            text_color=self.colors["text"],
            font=("Arial", 16, "bold"),
            command=lambda t=text: self.on_button_click(t)
        )
        btn.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)

    def on_button_click(self, text):
        if text == "AC":
            self.expression = ""
            self.display_var.set("")
            self.result_var.set("0")
        elif text == "DEL":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression)
            self.update_preview()
        elif text == "=":
            self.calculate()
        elif text == "x²":
            self.expression += "**2"
            self.display_var.set(self.expression)
            self.update_preview()
        elif text == "xʸ":
            self.expression += "**"
            self.display_var.set(self.expression)
            self.update_preview()
        elif text == "!":
            self.expression += "!"
            self.display_var.set(self.expression)
            self.update_preview()
        elif text == "pi":
            self.expression += "pi"
            self.display_var.set(self.expression)
            self.update_preview()
        elif text == "e":
            self.expression += "e"
            self.display_var.set(self.expression)
            self.update_preview()
        else:
            self.expression += text
            self.display_var.set(self.expression)
            self.update_preview()

    def update_preview(self):
        try:
            temp_expr = prepare_expression(self.expression)
            if temp_expr.strip():
                result = eval(temp_expr, {"__builtins__": None}, self.safe_dict)
                self.result_var.set(str(result))
            else:
                self.result_var.set("0")
        except:
            self.result_var.set("")

    def calculate(self):
        try:
            expr = prepare_expression(self.expression)
            result = eval(expr, {"__builtins__": None}, self.safe_dict)

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.result_var.set(str(result))
            self.history.append(f"{self.expression} = {result}")
            self.history_label.configure(text=self.history[-1])

            self.expression = str(result)
            self.display_var.set(self.expression)

        except Exception:
            messagebox.showerror("Error", "Invalid expression")
            self.result_var.set("Error")

    def bind_keys(self):
        self.bind("<Key>", self.key_press)
        self.bind("<Return>", lambda event: self.calculate())
        self.bind("<BackSpace>", lambda event: self.delete_last())
        self.bind("<Escape>", lambda event: self.clear_all())

    def key_press(self, event):
        allowed = "0123456789+-*/()."
        if event.char in allowed:
            self.expression += event.char
            self.display_var.set(self.expression)
            self.update_preview()
        elif event.char.lower() == "p":
            self.expression += "pi"
            self.display_var.set(self.expression)
            self.update_preview()

    def delete_last(self):
        self.expression = self.expression[:-1]
        self.display_var.set(self.expression)
        self.update_preview()

    def clear_all(self):
        self.expression = ""
        self.display_var.set("")
        self.result_var.set("0")