import pandas
import numpy as np
import math
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.patches as mp

#prices = pandas.read_csv(r"C:\Users\Anton Luca-Dorin\My Files\KINGS\Hackathons\Local Hack Day\Local-Hack-Day-master\Git\prices.csv")

class Table:
    def __init__(self, path):
        self.path = path
        self.prices = pandas.read_csv(path, "r")
        #self.lst = self.prices.iloc[0,0].split(',')

class Column:
    def __init__ (self, code, dict, table) :
        self.code = code
        self.lst = []
        self.index = dict.code_to_index[code]
        self.calculate_column_avg(self.index, table)
        self.calculate_list(self.index, table)
        self.volatility = calculate_volatility(self.lst)
        self.volat_PROCENT = calculate_volatility_PROCENTS(self.lst)


    def calculate_column_avg(self, column, table):
        avg = 0
        index = 0
        for x in range(0,31):
            if not math.isnan(float(table.prices.iloc[x,0].split(',')[column])):
                avg += float(table.prices.iloc[x,0].split(',')[column])
                index += 1
        self.avg = avg/index;

    def calculate_list(self, column, table):
          for x in range(0,31):
            if not math.isnan(float(table.prices.iloc[x,0].split(',')[column])):
                self.lst.append(float(table.prices.iloc[x,0].split(',')[column]))
            else:
                self.lst.append(calculate_column_avg(column))

    def print_all(self):
        print(self.code)
        print()
        print(self.lst)
        print()
        print(self.index)
        print()
        print(self.avg)
        print()

class Dictionaries:

    def __init__(self, path):
        self.path = path
        self.file = open(path, "r")
        self.lines = []
        self.codes = []
        self.code_to_index = {}
        self.index_to_code = {}
        self.code_to_name = {}
        self.name_to_code = {}
        self.code_to_sector = {}
        self.create_stuff()

    def create_lines(self, lines):
        for line in self.file:
            lines.append(line.split('\n'))

    def create_codes(self, codes):
        for element in self.lines:
            lst = element[0].split(' ')
            codes.append(lst[0])

    def create_dictionaries(self, lines):
        aux = []
        for i in range(0,90):
            aux += lines[i][0].split(' ')

        for i in range(0,len(aux),3):
            self.code_to_index[aux[i]] = int(i/3)
            self.index_to_code[int(i/3)] = aux[i]
            self.code_to_name[aux[i]] = aux[i+1]
            self.name_to_code[aux[i+1]] = aux[i]
            self.code_to_sector[aux[i]] = aux[i+2]

    def create_stuff(self):
        self.create_lines(self.lines)
        self.create_codes(self.codes)
        self.create_dictionaries(self.lines)

    def print_all(self):
        print("Code to sector:\n")
        print(self.code_to_sector)
        print("Name to code:\n")
        print(self.name_to_code)
        print("Code to name:\n")
        print(self.code_to_name)
        print("Code to index:\n")
        print(self.code_to_index)
        print("Codes:\n")
        print(self.codes )
        print("Lines:\n")
        print(self.lines)

class Query:

    def __init__(self):
        self.lowest_volat = []
        self.highest_volat = []
        self.avg_volat = 0
        self.lowest_codes = []
        self.highest_codes = []
        self.ordered_columns = []
        self.ordered_volats = []

    def append_to_lowest(self, value, code):
        self.lowest_volat.append(value)
        self.lowest_codes.append(code)

    def append_to_highest(self, value, code):
        self.highest_volat.append(value)
        self.highest_codes.append(code)

    def print_all(self):
        print("Lowest volailities: ")
        print(self.lowest_volat)
        print()
        print("Lowest codes:")
        print(self.lowest_codes)
        print()
        print("Highest volatilities: ")
        print(self.highest_volat)
        print()
        print("Highest codes: ")
        print(self.highest_codes)
        print()
        print("Average Volatility: ")
        print(self.avg_volat)
        print()
        print("Ordered columns: ")
        print(self.ordered_columns)
        print()
        print("Ordered volatilities: ")
        print(self.ordered_volats)



def calculate_volatility(lst = []):
    return np.diff(np.log(lst)).std()*np.sqrt(12)

def calculate_volatility_PROCENTS(lst = []):
    var = np.diff(np.log(lst)).std()*np.sqrt(12)*100
    return var
    #print(str(var) + " %")

def plot_graph(column, dict):
    val_lst = column.lst
    date_lst = []
    date = dt.datetime.now()
    date -= dt.timedelta(days = 30)
    date_lst.append(date)
    for ini in range(0,len(val_lst)-1):
        date += dt.timedelta(days = 1)
        date_lst.append(date)
    #result = [date_lst,val_lst,code_to_name[column_code]]
    #return result
    #print (date_lst)
    plt.plot(date_lst, val_lst, "b-")
    blue_patch = mp.Patch(color = "blue", label = dict.code_to_name[column.code])
    plt.legend(handles = [blue_patch])
    plt.show()

def mean_volatility(columns):
    volat_avg = 0
    index = 0
    volat = []
    for column in columns:

        volat_avg += column.volatility
        volat.append(column.volatility)
        index += 1
    for x in range(0,len(columns)-1):
        for y in range(x,len(columns)):
            if volat[x] > volat[y]:
                volat[x],volat[y] = volat[y],volat[x]
                aux = columns[x]
                columns[x] = columns[y]
                columns[y] = aux
    
    l = len(columns)
    if l >= 6:
        result = Query()
        for i in range(0 , 3):
            result.append_to_lowest(volat[i],columns[i].code)
            result.append_to_highest(volat[len(columns)-i-1], columns[len(columns)-i-1].code)

        result.avg_volat = volat_avg/index
        result.ordered_columns = columns
        result.ordered_volats = volat
        return result
    else: return None
#MAIN ______________________________________________________________________________________________________________
#for x in range(0, 90):
#    lst = []
#    calculate_list(x,lst)
#    np_lst= np.array(lst)
#    print("Nr:" + str(x))
#    display_diff(np_lst)

test = Dictionaries(r"C:\Users\Anton Luca-Dorin\My Files\KINGS\Hackathons\Local Hack Day\Local-Hack-Day-master\Git\codes.txt")
test.create_stuff()

table = Table(r"C:\Users\Anton Luca-Dorin\My Files\KINGS\Hackathons\Local Hack Day\Local-Hack-Day-master\Git\prices.csv")
lst = []

for i in range(0,10):
    col = Column(test.index_to_code[i],test,table)
    lst.append(col)

query = mean_volatility(lst)

query.print_all()

#plot_graph(objCol, test)

# print(aux)
#print()
#print(code_to_name)
#print()
#print(name_to_code)
#print()
#print(code_to_sector)
#print()
#print(code_to_index)
#print()
#print(plot_graph("MSFT"))
#print(mean_volatility(["MSFT","T","FB","ORCL","CSCO","NVDA","MCRO.L"]))
