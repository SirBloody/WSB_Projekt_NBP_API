import httpx

def get_rates(selected_date, currency, amount, attempt=0):
   try:
       # If amount blank, then amount = 1
       if amount == "":
           amount = 1
       url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{selected_date}"
       resp = httpx.get(url)
       resp.raise_for_status()
       data = resp.json()
       rate = data['rates'][0]['mid']
       return rate, selected_date, amount
       # output_text.delete(1.0, tk.END)
       # output_text.insert(tk.END, f'Exchange rate for 1 {currency}: {rate} PLN\n')
       # output_text.insert(tk.END, f'Date: {selected_date}\n')
       # output_text.insert(tk.END, f'{amount} {currency} = {float(amount)*rate} PLN')
   except httpx.HTTPStatusError:
       if attempt < 7:
           prev_date = (datetime.strptime(selected_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
           return self.get_rates(prev_date, currency, amount, attempt + 1)
       else:
           return None, None, None
#              self.output_text.delete(1.0, tk.END)
#              self.output_text.insert(tk.END, f'Error: No exchange rates found for selected date or nearby dates \n')
   except httpx.RequestError:
#          self.output_text.delete(1.0, tk.END)
#          self.output_text.insert(tk.END, f'Error: Request failed. Please check your internet connection.\n')
        return None, None, None