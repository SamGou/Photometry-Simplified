import tkinter as tk
from tkinter import filedialog
import xlrd
import pandas as pd
import numpy as np
import os
import csv
from func_for_csv import index, trns_tableTocsv
from Main_2 import aperture_file

root = tk.Tk()
root.title("Photometry Simplified")

canvas1 = tk.Canvas(root, bg='lightsteelblue')
canvas1.pack(fill="x")
canvas2 = tk.Canvas(root, bg="green")
canvas2.pack()

table1 = 0
table2 = 0
table3 = 0
table_sum = 0

B_path = None  # Filter 1 path
V_path = None  # filter 2 path
res = None
topcat_data = None
BPRP_path = None
filter = tk.StringVar()  # variable for radiobuttons
filter.set("BV")  # initiallise
excess = tk.DoubleVar()
distance = tk.DoubleVar()
distance.set(10.0)


def getExceltableB():
    global table1
    global B_path
    global table_sum
    import_file_path = filedialog.askopenfilename()
    B_path = str(import_file_path)
    table1 += 1
    table_sum = table1 + table2 + table3
    if table_sum == 3:
        canvas1.create_window(400, 230, window=Ok_button)


def getExceltableV():
    global table2
    global V_path
    global table_sum
    import_file_path = filedialog.askopenfilename()
    V_path = str(import_file_path)
    table2 += 1
    table_sum = table1 + table2 + table3
    if table_sum == 3:
        canvas1.create_window(400, 230, window=Ok_button)


def Ok():
    global B_path
    global V_path
    global res
    global BPRP_path
    global filter
    res = slider.get()
    excess = float(entry_excess.get())
    distance = float(entry_distance.get())
    trns_tableTocsv(B_path, V_path, BPRP_path, filter.get(), res, excess,distance)
    # root.destroy()


def RADEC():
    global topcat_data
    import_file_path = filedialog.askopenfilename()
    topcat_data = str(import_file_path)
    aperture_file(topcat_data)


def getExceltableTOPCAT():
    global BPRP_path
    global table3
    global talbe_sum
    import_file_path = filedialog.askopenfilename()
    BPRP_path = str(import_file_path)
    table3 += 1
    table_sum = table1 + table2 + table3
    if table_sum == 3:
        canvas1.create_window(400, 230, window=Ok_button)


label_slider = tk.Label(canvas2, text="Magnitude Limit")
label_slider.pack(side="left")
slider = tk.Scale(canvas2, from_=0, to=20, orient="horizontal", length=700)
slider.pack(side="left")


def split(word):
    return list(word.get())


filter_list = split(filter)


browseButton_ExcelV = tk.Button(text='Import {} table'.format(filter_list[1]), command=getExceltableV,
                                bg='green', fg='white', font=('helvetica', 12, 'bold'))

browseButton_ExcelB = tk.Button(text='Import {} table'.format(filter_list[0]), command=getExceltableB,
                                bg='blue', fg='white', font=('helvetica', 12, 'bold'))

browseButton_ExcelTOPCAT = tk.Button(text='Import Topcat data', command=getExceltableTOPCAT,
                                     bg='chocolate3', fg='white', font=('helvetica', 12, 'bold'))

RADEC_button = tk.Button(text='Create Aperture File', command=RADEC,
                         bg='red', fg='white', font=('helvetica', 12, 'bold'))

Ok_button = tk.Button(text='OK', command=Ok, bg='black',
                      fg='white', font=('helvetica', 12, 'bold'))


def update(button1=browseButton_ExcelB, button2=browseButton_ExcelV, text=filter_list):
    filter_list = split(filter)
    text = filter_list
    button1.config(text="Import {} table".format(text[0]))
    button2.config(text="Import {} table".format(text[1]))


radioBR = tk.Radiobutton(root, text="Filters: B and R", variable=filter,
                         value="BR", command=update)
radioBR.pack(side="left")
radioBV = tk.Radiobutton(root, text="Filters: B and V", variable=filter,
                         value="BV", command=update)
radioBV.pack(side="left")

# distance
label_distance = tk.Label(root, text="Distance to cluster(pc)")
entry_distance = tk.Entry(root,textvariable = distance)
entry_distance.pack(side="right")
label_distance.pack(side="right")
# excess
label_excess = tk.Label(root, text="Colour excess E(B-V)")
entry_excess = tk.Entry(root,textvariable = excess)
entry_excess.pack(side="right")
label_excess.pack(side="right")


canvas1.create_window(400, 180, window=browseButton_ExcelB)
canvas1.create_window(400, 130, window=browseButton_ExcelV)
canvas1.create_window(400, 80, window=RADEC_button)
canvas1.create_window(400, 30, window=browseButton_ExcelTOPCAT)


root.mainloop()
