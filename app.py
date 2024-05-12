import tkinter as tk
from tkinter import ttk
import httpx
from tkcalendar import Calendar
from datetime import datetime, timedelta, date
from tkinter import font
import import_from_file_to_list
import prevents


root = tk.Tk()
root.resizable(False, False)
root.title("Convert currency to Polish zloty")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 700
window_height = 700
large_font = font.Font(family="Helvetica", size=16)

#Window in the center of screen

center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')



#Used for preventing user from choosing the future dates
today = date.today()


#Import currencies
currencies = import_from_file_to_list.import_data('currencies.txt')

#Import currencies names
name = import_from_file_to_list.import_data('currency_name.txt')



combo_val = tk.StringVar()
combo_val.set(currencies[9]) #Default currency: EUR


def dynamic_label(event):
    selected_index = combo_box.current()
    if selected_index >= 0 and selected_index < len(name):
        label3.config(text=f'Currency name: {name[selected_index]}')

#Parameter attempt is for preventing recursion loop

def get_rates(selected_date, currency, amount, attempt=0):
    try:
        #If amount blank, then amount = 1
        if amount == "":
            amount = 1
        url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{selected_date}"
        resp = httpx.get(url)
        resp.raise_for_status()
        data = resp.json()
        rate = data['rates'][0]['mid']
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f'Exchange rate for 1 {currency}: {rate} PLN\n')
        output_text.insert(tk.END, f'Date: {selected_date}\n')
        output_text.insert(tk.END, f'{amount} {currency} = {float(amount)*rate} PLN')
    except httpx.HTTPStatusError:
        if attempt < 7:
            prev_date = (datetime.strptime(selected_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
            get_rates(prev_date, currency, amount, attempt + 1)
        else:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f'Error: No exchange rates found for selected date or nearby dates \n')
    except httpx.RequestError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f'Error: Request failed. Please check your internet connection.\n')

#Create variable to store entry
input_var = tk.StringVar()

#Create variable for validation in entry box
validate = root.register(prevents.validate_num)

cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd", maxdate=today)
cal.grid(row=1 ,column=3 ,padx=100, pady=10)

label = tk.Label(root, text='Choose date and currency to fetch data', font=large_font)
label.grid(row=0, column=3, padx=150, pady=10)

label2 = tk.Label(root, text="Amount of currency: ", font=large_font)
label2.grid(row= 2, column=3, padx=150, pady=10)

entry = tk.Entry(root, textvariable=input_var, validate="key", validatecommand=(validate, '%P'))
entry.grid(row= 3, column= 3, padx=150, pady=20)

label3 = tk.Label(root, text="Currency name: Euro", font=large_font)
label3.grid(row=4, column= 3, padx= 150, pady=20)

combo_box = ttk.Combobox(root, textvariable=combo_val, values= currencies, state='readonly')
combo_box.grid(row= 5,column= 3, padx=150, pady=20)

output_text = tk.Text(root, height=5, width=40)
output_text.grid(row= 7, column= 3, padx=150, pady=5)

get_rates_button = tk.Button(root, text="Get Exchange Rate", command=lambda: get_rates(cal.get_date(), combo_val.get(), entry.get()))
get_rates_button.grid(row= 6, column= 3, pady=20)


#Bind preventing function to output widget
output_text.bind("<Key>", prevents.on_key)
#Bind selected value from combobox with dynamic_label (label3)
combo_box.bind("<<ComboboxSelected>>", dynamic_label)

root.mainloop()
