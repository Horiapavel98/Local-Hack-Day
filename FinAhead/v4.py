import pandas
import numpy as np
import math
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.patches as mp

#prices = pandas.read_csv(r"C:\Users\Anton Luca-Dorin\My Files\KINGS\Hackathons\Local Hack Day\Local-Hack-Day-master\Git\prices.csv")
#_______CREATES A TABLE TO READ FROM
class Table:
    def __init__(self, path):
        self.path = path
        self.prices = pandas.read_csv(path, "r")
        #self.lst = self.prices.iloc[0,0].split(',')
#________COLUMN CLASS PREPARES EVERYTHING THAT IS NEEDED TO ACCESS AND COMPUTE THE COLUMN FROM THE TABLE
class Column:
    def __init__ (self, code, dict, table) :
        self.code = code
        self.lst = []
        self.index = dict.code_to_index[code]
        self.calculate_column_avg(self.index, table)
        self.calculate_list(self.index, table)
        self.damage_control()
        self.volatility = calculate_volatility(self.lst)
        self.volat_PROCENT = calculate_volatility_PROCENTS(self.lst)


    def calculate_column_avg(self, column, table):
        avg = 0
        index = 0
        for x in range(0,31):
            if not table.prices.iloc[x,0].split(',')[column] == "":
                #print(table.prices.iloc[x,0].split(',')[column])
                avg += float(table.prices.iloc[x,0].split(',')[column])
                index += 1
        if index is not 0:
            self.avg = avg/index
        else:
            self.avg = avg

    def calculate_list(self, column, table):
          for x in range(0,31):
            if not table.prices.iloc[x,0].split(',')[column] == "":
                self.lst.append(float(table.prices.iloc[x,0].split(',')[column]))
            else:
                self.lst.append(self.calculate_column_avg(column, table))
        #    if table.prices.iloc[x,0].split(',')[column] == "":
        #        print("YES")
        #    else:
        #        print("NO")

    def damage_control(self):
        index = None
        for item in self.lst:
            if item is None:
                index = self.lst.index(item)
                break
        if index is not None:
            self.lst[index] = self.avg
            self.damage_control()

    def print_all(self):
        print(self.code)
        print()
        print(self.lst)
        print()
        print(self.index)
        print()
        print(self.avg)
        print()
#________DICTIONARY CLASS PREPARES ALL THE DICTIONARIES THAT ARE NEEDED DURING THE ANALYZING PART
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
#_______QUERY CLASS PREPARES THE RESULT FOR THE mean_volatility METHOD DEFINED BELOW.
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


#_______OTHER USEFUL METHODS.
def calculate_volatility(lst):
    return np.diff(np.log(lst)).std()*np.sqrt(12)


def calculate_volatility_PROCENTS(lst):
    var = np.diff(np.log(lst)).std()*np.sqrt(12)*100
    return var


def plot_graph(column, dict):
    val_lst = column.lst
    date_lst = []
    date = dt.datetime.now()
    date -= dt.timedelta(days = 30)
    date_lst.append(date)
    for ini in range(0,len(val_lst)-1):
        date += dt.timedelta(days = 1)
        date_lst.append(date)

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
