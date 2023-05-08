import tkinter
import random
import openpyxl
import os
import pandas as pd
import algorithmtwo
import time
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

excel_tag = 1
flag = 1

def on_validate_k(value):
    if value.isdigit() and int(value) >= 4 and int(value) <= 7:
        return True
    else:
        return False
    
    
def on_validate_j(value):
    if value.isdigit() and int(value) >= 3 and int(value) <= int(Parameters_third_combobox.get()):
        return True
    else:
        return False
    
    
def on_validate_s(value):
    if value.isdigit() and int(value) >= 3 and int(value) <= int(Parameters_fourth_combobox.get()):
        return True
    else:
        return False


def generate_number_n():
    number = random.randint(7,25)
    number_entry.delete(0,tkinter.END)
    number_entry.insert(0,str(number))


def generate_total_sample():  #total m samples
    total = int(Parameters_one_Combobox.get())
    total_list = list(range(1,total+1))
    return total_list


def generate_n_sample(total_list):
    n_values = int(number_entry.get())
    select_n_samples = random.sample(total_list,n_values)
    select_n_samples.sort()
    return select_n_samples


def enter_data():
    # global m,n,k,j,s
    m = Parameters_one_Combobox.get()
    n = number_entry.get()
    k = Parameters_third_combobox.get()
    j = Parameters_fourth_combobox.get()
    s = Parameters_fifth_combobox.get()
    # total_samples = generate_total_sample()
    # n_samples = generate_n_sample(total_samples)
    
    if m and n and s and j and k: 
        flag = 1 
    else:
        flag = 0
        tkinter.messagebox.showwarning(title="Error",message="You should enter the value in all boxes!")
    
    return flag

def output_n_samples():
    total_samples = generate_total_sample()
    for item in total_samples:
        output_n_samples.insert(tkinter.END, ",".join(str(x) for x in item) + "\n")

def import_excel():
    global excel_tag
    #import the excel file you may want
    file_path = filedialog.askopenfilename(title="Select Excel file",filetypes=(("Excel files", "*.xlsx"), ("all files", "*.*")))
    
    if(file_path):
        excel_tag = 1
    if file_path:
        print(f"Selected file: {file_path}")
        df_import = pd.read_excel(file_path)

       
        # get the data of each column from the newest row
        
        global last_row
        last_row = df_import.iloc[-1] 

        data_dictionary = {}
        for i,col in enumerate(df_import.columns):
            data_dictionary[col] = last_row[i]
        
        k_value = data_dictionary['k']
        j_value = data_dictionary['j']
        
        Parameters_one_Combobox.config(state="normal")
        Parameters_one_Combobox.insert(0, last_row['m'])
        Parameters_one_Combobox.config(state="readonly")
        
        number_entry.insert(0, last_row['n'])
        number_entry.config(state="readonly")

        Parameters_third_combobox.config(state="normal")
        Parameters_third_combobox.insert(0, last_row['k'])
        Parameters_third_combobox.config(state="readonly")
        
        Parameters_fourth_combobox.config(values=list(range(3, int(k_value) + 1)))
        Parameters_fourth_combobox.config(state="normal")
        Parameters_fourth_combobox.insert(0, last_row['j'])
        Parameters_fourth_combobox.config(state="readonly")

        Parameters_fifth_combobox.config(values=list(range(3, int(k_value) + 1)))
        Parameters_fifth_combobox.config(state="normal")
        Parameters_fifth_combobox.insert(0, last_row['s'])
        Parameters_fifth_combobox.config(state="readonly")
        
    else:
        print("No file selected.")
    return excel_tag
 
def output_data():
    if enter_data() == 1:
        m = int(Parameters_one_Combobox.get())
        n = number_entry.get()
        k = Parameters_third_combobox.get()
        j = Parameters_fourth_combobox.get()
        s = Parameters_fifth_combobox.get()
        total_samples = generate_total_sample()
        n_samples = generate_n_sample(total_samples)
        
      
        # Core Algorithm and count executing time
        start_time = time.time()
        data_list = algorithmtwo.get(m,int(n),int(k),int(j),int(s))
        end_time = time.time()
        duration = end_time - start_time
       
        
        total_str_list = []
        for i in range(0,len(data_list)):
            total_str_list.append([0]* int(k))
            h = 0
            for p in range(0,int(n)):
                if data_list[i][p] == '1':
                    total_str_list[i][h] = n_samples[p]
                    h += 1
        
        result_list_count = 0
        
        for item in n_samples:
            output_n_samples.insert(tkinter.END, ','.join(str(x) for x in n_samples) + "\n")
          
        # traverse the data in the list and output them in the window
        for item in total_str_list:
            output_frame_text.insert(tkinter.END, ",".join(str(x) for x in item) + "\n")
            result_list_count += 1
        output_frame_text.insert(tkinter.END, f"Total results: {result_list_count}" + "\n")
        output_frame_text.insert(tkinter.END, f"Algorithm running time: {duration}s")
        
        
        
        #import all input and output to excel
        filepath = "D:\MUST 2302学期\人工智能\Group Project(v1.0.6)\output.xlsx"
        
        if not os.path.exists(filepath):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            heading = ["m","n","k","j","s","running time","total_samples","n samples out of total samples","output numbers","output result"]
            sheet.append(heading)
            workbook.save(filepath)
        workbook = openpyxl.load_workbook(filepath)
        sheet = workbook.active
        data = [m,n,k,j,s,duration,','.join(map(str,total_samples)),','.join(map(str,n_samples)),result_list_count,','.join(map(str,total_str_list))]  #map will convert the int type to string type
        sheet.append(data)
        workbook.save(filepath)
    else:
        tkinter.messagebox.showwarning(title="Error",message="Error! No output!")


def clear_all_input():
    Parameters_one_Combobox.set('')
    number_entry.config(state="normal")
    number_entry.delete(0,tkinter.END)
    Parameters_third_combobox.set('')
    Parameters_fourth_combobox.set('')
    Parameters_fourth_combobox.config(state="disable")
    Parameters_fifth_combobox.set('')
    Parameters_fifth_combobox.config(state="disable")


#delete the content from the 1st row 1st column to the last character
def clear_output():
    output_n_samples.delete('1.0',tkinter.END)
    output_frame_text.delete('1.0', tkinter.END)


'''
create a top-level window object using the tkinter module in Python
for creating GUI applications
'''

if __name__ == '__main__':
    window = tkinter.Tk()
    window.title("Optimal Sample Selection System")


    frame = tkinter.Frame(window)
    frame.pack()
    frame.configure(bg="#FFFFFF")
    
    # Saving User Info
    # 1: First Label Frame
    Parameters_info_frame = tkinter.LabelFrame(frame,font=("Helvetica", 14), bg="#FFE0B2", fg="#333333",text="Parameter Information")  #grid title
    Parameters_info_frame.grid(row=0,column=0,sticky="news",padx=20,pady=20)

    Parameters_one_label = tkinter.Label(Parameters_info_frame,font=("Helvetica", 14), bg="#FFE0B2", fg="#333333",text="m")
    Parameters_one_label.grid(row=0,column=0,sticky="news",padx=20,pady=20)
    
    Parameters_one_Combobox = ttk.Combobox(Parameters_info_frame,font=("Helvetica", 14),values=[45,46,47,48,49,50,51,51,53,54],state="readonly")
    Parameters_one_Combobox.grid(row=1,column=0,sticky="news",padx=20,pady=20)


    Parameters_second_label = tkinter.Label(Parameters_info_frame,font=("Helvetica", 14), bg="#FFE0B2", fg="#333333",text="n")
    Parameters_second_label.grid(row=0,column=1,sticky="news",padx=20,pady=20)
    #Parameters_second_spinbox = ttk.Spinbox(Parameters_info_frame,from_=7,to=25)
    number_entry = tkinter.Entry(Parameters_info_frame, width=5, font=("Helvetica", 14))
    number_entry.grid(row=1,column=1,sticky="news",padx=20,pady=20)
    number_button = tkinter.Button(Parameters_info_frame,text="Generate a number for n",font=("Helvetica", 14), bg="#1E88E5", fg="white", command=generate_number_n)
    number_button.grid(row=1,column=2)


    Parameters_third_label = tkinter.Label(Parameters_info_frame,font=("Helvetica", 14), bg="#FFE0B2", fg="#333333",text="k")
    Parameters_third_label.grid(row=2,column=0)
    k_values=list(range(4,8))
    Parameters_third_combobox = ttk.Combobox(Parameters_info_frame,values=k_values,validate="key",font=("Helvetica", 14),validatecommand=(Parameters_info_frame.register(on_validate_k), '%P'),state="readonly")
    Parameters_third_combobox.grid(row=3,column=0,sticky="news",padx=20,pady=20)


    Parameters_fourth_label = tkinter.Label(Parameters_info_frame,font=("Helvetica", 14), bg="#FFE0B2", fg="#333333",text="j")
    Parameters_fourth_label.grid(row=2,column=1,sticky="news",padx=20,pady=20)
    j_values= list(range(3,8))
    Parameters_fourth_combobox = ttk.Combobox(Parameters_info_frame,values=j_values,validate="key",font=("Helvetica", 14),validatecommand=(Parameters_info_frame.register(on_validate_j), '%P'), state="disabled")
    Parameters_fourth_combobox.grid(row=3,column=1,sticky="news",padx=20,pady=20)


    Parameters_fifth_label = tkinter.Label(Parameters_info_frame,font=("Helvetica", 14), bg="#FFE0B2", fg="#333333",text="s")
    Parameters_fifth_label.grid(row=2,column=2,sticky="news",padx=20,pady=20)
    s_values = list(range(3))
    Parameters_fifth_combobox = ttk.Combobox(Parameters_info_frame,values=s_values,validate="key",font=("Helvetica", 14),validatecommand=(Parameters_info_frame.register(on_validate_s), '%P'), state="disabled")
    Parameters_fifth_combobox.grid(row=3,column=2,sticky="news",padx=20,pady=20)
    
    import_excel_button = tkinter.Button(Parameters_info_frame, text="Import Excel Data", command=import_excel, font=("Helvetica", 10), bg="#1E88E5", fg="white")
    import_excel_button.grid(row=4, column=0, sticky="news", padx=20, pady=20)
    button = tkinter.Button(Parameters_info_frame,text="Enter data",font=("Helvetica", 10), bg="#1E88E5", fg="white", activebackground="#1565C0", activeforeground="white",command=enter_data)
    button.grid(row=4,column=1,sticky="news",padx=20,pady=20)
    
    clear_input_button = tkinter.Button(Parameters_info_frame,text="Clear all input",font=("Helvetica", 10), bg="#1E88E5", fg="white", activebackground="#1565C0", activeforeground="white",command=clear_all_input)
    clear_input_button.grid(row=4,column=2,sticky="news",padx=20,pady=20)
    
    for widget in Parameters_info_frame.winfo_children():
        widget.grid_configure(padx=10,pady=5) #set 'padx' (horizontal outer margin) to 10 pixels and 'pad' (vertical outer margin) to 5 pixels.


    # Define a callback function for input box k to enable input box j
    def on_k_changed(event):
        j_values.clear()
        k_value = int(Parameters_third_combobox.get())
        j_values.extend(list(range(3,k_value+1)))
        Parameters_fourth_combobox.config(values=j_values)
        Parameters_fourth_combobox.config(state="readonly")
    # Callback function for binding input box k

    Parameters_third_combobox.bind("<<ComboboxSelected>>", on_k_changed)


    
    # Define a callback function for input box j to enable input box s
    def on_j_changed(event):
        s_values.clear()
        j_value = int(Parameters_fourth_combobox.get())
        s_values.extend(list(range(3, j_value+1)))
        Parameters_fifth_combobox.config(values=s_values)
        Parameters_fifth_combobox.config(state="readonly")
    # Callback function for binding input box j
    Parameters_fourth_combobox.bind("<<ComboboxSelected>>", on_j_changed)


    #2: Second Label Frame
    
    output_frame = tkinter.LabelFrame(frame,font=("Helvetica", 14), bg="#FFE0B2", fg="#333333",text="Output Information")  #grid title
    output_frame.grid(row=4,column=0,sticky="news",padx=20,pady=20)
    
    output_n_label = tkinter.Label(output_frame,font=("Helvetica", 14), bg="#FFE0B2", fg="#333333",text="n out of m samples")
    output_n_label.grid(row=0,column=0,sticky="news",padx=20,pady=20)
    output_n_samples = tkinter.Text(output_frame,font=("Helvetica",14),height=1,width=50)
    output_n_samples.grid(row=1,column=0,sticky="news",padx=20,pady=20)
    
    output_final_label = tkinter.Label(output_frame,font=("Helvetica", 14), bg="#FFE0B2", fg="#333333",text="Final Samples")
    output_final_label.grid(row=2,column=0,sticky="news",padx=20,pady=20)
    output_frame_text = tkinter.Text(output_frame,font=("Helvetica", 14),height=8,width=50)
    output_frame_text.grid(row=3,column=0,sticky="news",padx=20,pady=20)

    scrollbar = tkinter.Scrollbar(output_frame, command=output_frame_text.yview)
    scrollbar.grid(row=3, column=1, sticky='nsew',padx=20,pady=20)
    output_frame_text['yscrollcommand'] = scrollbar.set
   

    generate_output_button = tkinter.Button(output_frame,text="Click to generate output",font=("Helvetica", 10), bg="#1E88E5", fg="white", activebackground="#1565C0", activeforeground="white",command=output_data)
    generate_output_button.grid(row=4,column=0,sticky="news",padx=20,pady=20)

    generate_output_clear_button = tkinter.Button(output_frame,text="Clear all output",font=("Helvetica", 10), bg="#1E88E5", fg="white", activebackground="#1565C0",command=clear_output)
    generate_output_clear_button.grid(row=5,column=0,sticky="news",padx=20,pady=20)
    
    
    frame.quit()


    #start the main event loop of the application, in order to handle user interactions and other events
    window.mainloop() 

