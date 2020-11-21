import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import StringVar
import pandas as pd
from copy import deepcopy
import os

import apiInterface


root = tk.Tk()
global filepath
filepath = None
my_string_var = StringVar() 
my_string_var.set("Browse for a excel file from your system with GST data")

def showinstructions():
    messagebox.showinfo('Instructions', '1. Use Template to create an excel file\n2. Delete the sample data given in the template\n3. Save the template as new file and browse to it using the below button\n4. Press Start Searcing to generate search data and wait till it completes\n5. After Completing Search the folder with the file will open automatically')

def browsefile():
    global filepath
    filepath = filedialog.askopenfilename(title = "Select Data File")
    my_string_var.set(str(deepcopy(filepath)))
    
    

def showTemplate():
    print("Template Folder")
    os.system(f'start {os.path.realpath("./Template")}') 

def startsearch():
    global filepath
    
    if filepath==None:
        messagebox.showinfo("Error"," Please Select a File")
    else:
        #xlworkbook = pd.ExcelFile(filepath)
        df = pd.read_excel(filepath)
        rowlist = []
        for index,rows in df.iterrows():
            rowlist.append([rows[0],rows[1].replace(u'\xa0', u' ')])
        print(rowlist)
        apiInterface.getgstdata(rowlist)
        
        os.system(f'start {os.path.realpath("./Output")}')

      


root.title("GST Data Search")
root.minsize(500,300)
root.maxsize(500,300)
b = tk.Button(root,text="Instructions",command=showinstructions)
b.grid(row=2,column=2,columnspan=2,padx=10,pady=10)

template = tk.Button(root,text="Show Tempate",command=showTemplate)
template.grid(row=2,column=10,columnspan=2,padx=10,pady=10)

browselabel = tk.Label(root,textvariable = my_string_var).grid(row=4,column=7,columnspan=4,padx=10,pady=10)

browse = tk.Button(root,text="Browse",command=browsefile)
browse.grid(row=4,column=4,columnspan=2,padx=10,pady=10)


startsearchbutton = tk.Button(root,text="Start Search",command=startsearch)
startsearchbutton.grid(row=15,column=10,columnspan=2,padx=10,pady=10)
"""tk.Label(root,text="Enter Payslip Month and year").grid(columnspan=2,padx=10,pady=10)
tk.Label(root, text="Month").grid(row=1,padx=10,pady=10)
tk.Label(root, text="Year").grid(row=2,padx=10,pady=10)

e1 = tk.Entry(root)
e2 = tk.Entry(root)

e1.grid(row=1, column=1,padx=10,pady=10)
e2.grid(row=2, column=1,padx=10,pady=10)

b = tk.Button(root,text="Submit",command=generate)
b.grid(row=3,column=1,columnspan=2,padx=10,pady=10)
"""

root.mainloop()
