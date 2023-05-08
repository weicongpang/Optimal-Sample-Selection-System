import pandas as pd
import tkinter as tk

# create a window
window = tk.Tk()
window.title("Excel Data Reader")

# create variables to store data
data_dictionary = {}
current_row = -1

# function to read data from next row
def read_next_row():
    global current_row, data_dictionary
    current_row += 1
    if current_row >= df.shape[0]:
        return
    data_dictionary = {}
    for i, col in enumerate(df.columns):
        data_dictionary[col] = df.iloc[current_row, i]
    display_data()

# function to clear data
def clear_data():
    global data_dictionary
    data_dictionary = {}
    for entry in entries:
        entry.delete(0, tk.END)

# function to display data in entries
def display_data():
    for entry in entries:
        entry.delete(0, tk.END)
        entry.insert(0, data_dictionary[entry.name])

# read the excel file
df = pd.read_excel("test_case.xlsx")

# create entries for data display
entries = []
for i, col in enumerate(df.columns):
    tk.Label(window, text=col).grid(row=i, column=0, padx=10, pady=5)
    entry = tk.Entry(window, name=col)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

# create buttons
tk.Button(window, text="Read Next Row", command=read_next_row).grid(row=df.shape[1]+1, column=0, padx=10, pady=5)
tk.Button(window, text="Clear Data", command=clear_data).grid(row=df.shape[1]+1, column=1, padx=10, pady=5)

# start the main loop
window.mainloop()