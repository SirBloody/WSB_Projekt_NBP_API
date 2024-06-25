import tkinter as tk
from tkinter import ttk
import httpx
from tkcalendar import Calendar
from datetime import datetime, timedelta, date
from tkinter import font
import import_from_file_to_list
import prevents
import get_rates



class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Convert currency to Polish zloty")
        self.large_font = font.Font(family="Helvetica", size=16)
        self.resizable(False, False)
        self.screen_width = Application.winfo_screenwidth(self)
        self.screen_height = Application.winfo_screenheight(self)
        self.window_width = 700
        self.window_height = 700

        # Window in the center of the screen
        self.center_x = int(self.screen_width / 2 - self.window_width / 2)
        self.center_y = int(self.screen_height / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{self.center_x}+{self.center_y}')

        # Used for preventing user from choosing the future dates
        self.today = date.today()

        # Import currencies
        self.currencies = import_from_file_to_list.import_data('currencies.txt')
        # Import currencies names
        self.name = import_from_file_to_list.import_data('currency_name.txt')

        self.combo_val = tk.StringVar()
        self.combo_val.set(self.currencies[9])  # Default currency: EUR

        self.create_window()

    def create_window(self):
        self.cal = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd", maxdate=self.today)
        self.cal.grid(row=1, column=3, padx=100, pady=10)

        self.label = tk.Label(self, text='Choose date and currency to fetch data', font=self.large_font)
        self.label.grid(row=0, column=3, padx=150, pady=10)

        self.label2 = tk.Label(self, text="Amount of currency: ", font=self.large_font)
        self.label2.grid(row=2, column=3, padx=150, pady=10)

        self.input_var = tk.StringVar()
        self.validate = self.register(prevents.validate_num)
        self.entry = tk.Entry(self, textvariable=self.input_var, validate="key")
        self.entry.grid(row=3, column=3, padx=150, pady=20)

        self.label3 = tk.Label(self, text="Currency name: Euro", font=self.large_font)
        self.label3.grid(row=4, column=3, padx=150, pady=20)

        self.combo_box = ttk.Combobox(self, textvariable=self.combo_val, values=self.currencies, state='readonly')
        self.combo_box.grid(row=5, column=3, padx=150, pady=20)

        self.output_text = tk.Text(self, height=5, width=40)
        self.output_text.grid(row=7, column=3, padx=150, pady=5)

        self.get_rates_button = tk.Button(self, text="Get Exchange Rate", command=self.on_get_rate_button_click)
        self.get_rates_button.grid(row=6, column=3, pady=20)

        # Bind preventing function to output widget
        self.output_text.bind("<Key>", prevents.on_key)
        # Bind selected value from combobox with dynamic_label (label3)
        self.combo_box.bind("<<ComboboxSelected>>", self.dynamic_label)

    def dynamic_label(self, event):
        selected_index = self.combo_box.current()
        if selected_index >= 0 and selected_index < len(self.names):
            self.label3.config(text=f'Currency name: {self.names[selected_index]}')
    #def get_rates(self, selected_date, currency, amount, attempt=0):
    #    try:
    #        # If amount blank, then amount = 1
    #        if amount == "":
    #            amount = 1
    #        url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{selected_date}"
    #        resp = httpx.get(url)
    #        resp.raise_for_status()
    #        data = resp.json()
    #        rate = data['rates'][0]['mid']
    #        return rate, selected_date, amount
    #        # output_text.delete(1.0, tk.END)
    #        # output_text.insert(tk.END, f'Exchange rate for 1 {currency}: {rate} PLN\n')
    #        # output_text.insert(tk.END, f'Date: {selected_date}\n')
    #        # output_text.insert(tk.END, f'{amount} {currency} = {float(amount)*rate} PLN')
    #    except httpx.HTTPStatusError:
    #        if attempt < 7:
    #            prev_date = (datetime.strptime(selected_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    #            return self.get_rates(prev_date, currency, amount, attempt + 1)
    #        else:
    #            return None, None, None
#   #             self.output_text.delete(1.0, tk.END)
#   #             self.output_text.insert(tk.END, f'Error: No exchange rates found for selected date or nearby dates \n')
    #    except httpx.RequestError:
#   #         self.output_text.delete(1.0, tk.END)
#   #         self.output_text.insert(tk.END, f'Error: Request failed. Please check your internet connection.\n')
    #         return None, None, None

    def on_get_rate_button_click(self):
        selected_date = self.cal.get_date()
        currency = self.combo_val.get()
        amount = self.entry.get()
        rate, date, amount = get_rates.get_rates(selected_date, currency, amount)
        self.output_text.delete(1.0, tk.END)
        if rate is not None:
            self.output_text.insert(tk.END, f'Exchange rate for 1 {currency}: {rate} PLN\n')
            self.output_text.insert(tk.END, f'Date: {selected_date}\n')
            self.output_text.insert(tk.END, f'{amount} {currency} = {float(amount) * rate} PLN')
        else:
            self.output_text.insert(tk.END, 'Error: No exchange rates found for selected date or nearby dates \n')

if __name__ == "__main__":

    app = Application()
    app.mainloop()
