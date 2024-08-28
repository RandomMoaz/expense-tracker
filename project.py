import tkinter as tk
from tkinter import ttk

def add_expense():
    try:
        amount = float(amount_entry.get())
    except ValueError:
        status_label.config(text="Please enter a valid amount!", fg="red")
        return

    currency = currency_var.get()
    category = category_var.get()
    payment_method = payment_method_var.get()
    date = date_entry.get()
    
    # Convert the amount to USD for the total calculation
    usd_amount = convert_to_usd(amount, currency)
    
    # Add the data to the treeview
    expense_tree.insert("", "end", values=(f"{amount:.2f}", currency, category, payment_method))
    
    # Update the total in USD
    update_total(usd_amount)

def convert_to_usd(amount, currency):
    # Conversion rates as an example
    conversion_rates = {
        "USD": 1,
        "EUR": 1.1,
        "GBP": 1.3,
    }
    return amount * conversion_rates.get(currency, 1)

def update_total(new_amount):
    global total_usd
    total_usd += new_amount
    # Update the total row in the treeview
    expense_tree.item(total_row, values=(f"{total_usd:.2f}", "USD", "", ""))

def delete_expense():
    selected_item = expense_tree.selection()
    if selected_item:
        item_values = expense_tree.item(selected_item, "values")
        amount = float(item_values[0])
        currency = item_values[1]
        usd_amount = convert_to_usd(amount, currency)
        
        # Remove the selected item from the treeview
        expense_tree.delete(selected_item)
        
        # Update the total in USD
        update_total(-usd_amount)
    else:
        status_label.config(text="Please select an expense to delete!", fg="red")

# Main window
root = tk.Tk()
root.title("Expense Tracker")

# Set window size to a comfortable size (e.g., 600x400 pixels)
root.geometry("600x400")

# Create variables for the dropdowns
currency_var = tk.StringVar(value="USD")
category_var = tk.StringVar(value="Savings")
payment_method_var = tk.StringVar(value="Credit Card")

# Create and place the labels and entries with padding
tk.Label(root, text="Amount").grid(row=0, column=0, padx=10, pady=10)
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Currency").grid(row=1, column=0, padx=10, pady=10)
currency_dropdown = ttk.Combobox(root, textvariable=currency_var, values=["USD", "EUR", "GBP"])
currency_dropdown.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Category").grid(row=2, column=0, padx=10, pady=10)
category_dropdown = ttk.Combobox(root, textvariable=category_var, values=["Savings", "Rental", "Groceries"])
category_dropdown.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Payment Method").grid(row=3, column=0, padx=10, pady=10)
payment_method_dropdown = ttk.Combobox(root, textvariable=payment_method_var, values=["Credit Card", "Paypal", "Cash"])
payment_method_dropdown.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Date").grid(row=4, column=0, padx=10, pady=10)
date_entry = tk.Entry(root)
date_entry.grid(row=4, column=1, padx=10, pady=10)

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=5, column=0, columnspan=2, pady=10)

delete_button = tk.Button(root, text="Delete Expense", command=delete_expense)
delete_button.grid(row=5, column=1, pady=10)

columns = ("Amount", "Currency", "Category", "Payment Method")
expense_tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
for col in columns:
    expense_tree.heading(col, text=col)
expense_tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(1, weight=1)

total_usd = 0
total_row = expense_tree.insert("", "end", values=("0.00", "USD", "", ""), tags=('total',))
expense_tree.tag_configure('total', background='yellow')

status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()