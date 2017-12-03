from tkinter import *
import v4

#___DICTIONARIES_CREATED____
test = v4.Dictionaries(r"C:\Users\horia\Desktop\Local-Hack-Day\Local-Hack-Day-master\codes.txt")
test.create_stuff()

#____TABLE_FOR_READING_THE_DATA_CREATED______
table = v4.Table(r"C:\Users\horia\Desktop\Local-Hack-Day\Local-Hack-Day-master\prices.csv")

#____ORGANIZING_ALL_COLUMNS_IN_A_SINGLE_LIST_____

lst_col = []

for i in range(0,90):
    col = v4.Column(test.index_to_code[i],test,table)
    lst_col.append(col)

lst_names = []
for col in lst_col:
    lst_names.append(test.code_to_name[col.code])

OPTIONS = lst_names
#______GUI_INTERFACE____________________________________________________________________________
master = Tk("FinAhead")

variable = StringVar(master)
variable.set(OPTIONS[0]) # default value

w = OptionMenu(master, variable, *OPTIONS)
w.pack()

def ok():
    v4.plot_graph(lst_col[test.code_to_index[test.name_to_code[variable.get()]]],test)

def print_volat():
    string = str(lst_col[test.code_to_index[test.name_to_code[variable.get()]]].volat_PROCENT)
    string += "%"
    string2 = str(test.code_to_name[lst_col[test.code_to_index[test.name_to_code[variable.get()]]].code])
    string3 = str(lst_col[test.code_to_index[test.name_to_code[variable.get()]]].code)
    string4 = str(test.code_to_sector[lst_col[test.code_to_index[test.name_to_code[variable.get()]]].code])
    v.set(string)
    v1.set(string2)
    v2.set(string3)
    v3.set(string4)
    #label.grid(row = 3, column = 8)

button = Button(master, text="Plot", command=ok)
button2 = Button(master, text="Show Volatility", command=print_volat)
button.pack()
button2.pack()
v = StringVar()
v.set("")
v1 = StringVar()
v1.set("")
v2 = StringVar()
v2.set("")
v3 = StringVar()
v3.set("")
label = Label(master, textvariable = v)
label2 = Label(master, textvariable = v1)
label3 = Label(master, textvariable = v2)
label4 = Label(master, textvariable = v3)
label.pack()
label2.pack()
label3.pack()
label4.pack()


#_____SELECTION_PART_:_EXACTLY_6_SELECTIONS______
liste = Listbox(master,width=50, height=20,selectmode='multiple',exportselection=1)

for col in lst_col:
    index = test.code_to_index[col.code] + 1
    bag = str(test.code_to_name[col.code])
    liste.insert(END,bag)

items = []
def onselect(self):
    items.append(liste.get(liste.curselection()))
    if len(items) is  6:
        cols = []
        for itm in items:
            cols.append(lst_col[test.code_to_index[test.name_to_code[itm]]])
        result = v4.mean_volatility(cols)
        result.print_all()
    liste.selection_clear(0, END)

liste.bind('<<ListboxSelect>>', onselect)
liste.pack(padx=0, pady=0)

mainloop()
