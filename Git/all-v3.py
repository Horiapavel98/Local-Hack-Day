import pandas
import numpy as np
import math
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.patches as mp

prices = pandas.read_csv(r"C:\Users\horia\Desktop\Bank of America\prices.csv")

def calculate_column_avg(column):
    avg = 0
    index = 0
    for x in range(0,31):
        if not math.isnan(prices.iloc[x,column]):
            avg += prices.iloc[x,column]
            index += 1
    return avg/index

def calculate_list(column,lst_name = []):
      for x in range(0,31):
        if not math.isnan(prices.iloc[x,column]):
            lst_name.append(prices.iloc[x,column])
        else:
            lst_name.append(calculate_column_avg(column))

def calculate_diff(lst = []):
    return np.diff(np.log(lst)).std()*np.sqrt(12)

def display_diff(lst = []):
    var = np.diff(np.log(lst)).std()*np.sqrt(12)*100
    print(str(var) + " %")

def plot_graph(column_code):
    val_lst = []
    calculate_list(code_to_index[column_code], val_lst)
    date_lst = []
    date = dt.datetime(2017,10,17)
    date_lst.append(date)
    for ini in range(0,len(val_lst)-1):
        date += dt.timedelta(days = 1)
        date_lst.append(date)
    result = [date_lst,val_lst,code_to_name[column_code]]
    return result
#print (date_lst)
#    plt.plot(date_lst, val_lst, "b-")
#    blue_patch = mp.Patch(color = "blue", label = code_to_name[column_code])
#    plt.legend(handles = [blue_patch])
#    plt.show()

def mean_volatility(codes = []):
    avg = 0
    index = 0
    volat = []
    for code in codes:
        lst = []
        calculate_list(code_to_index[code], lst)
        avg = avg + calculate_diff(lst)
        volat.append(calculate_diff(lst))
        index += 1
    for x in range(0,len(codes)-1):
        for y in range(x,len(codes)):
            if volat[x] > volat[y]:
                volat[x],volat[y] = volat[y],volat[x]
                aux = codes[x]
                codes[x] = codes[y]
                codes[y] = aux
    print(volat)
    print()
    print(codes)
    print()
    if len(codes) < 5:
        result = []
        result.append(0)
        for i in range(0,len(codes)-1):
            result.append(codes[i])
            result.append(volat[i])
        result.append(avg/index)
    else:
        l = len(codes)
        result = [1,codes[0],volat[0],codes[1],volat[1],codes[2],volat[2],codes[l-3],volat[l-3],codes[l-2],volat[l-2],codes[l-1],volat[l-1], avg/index]
    return result
#MAIN ______________________________________________________________________________________________________________
for x in range(0, 90):
    lst = []
    calculate_list(x,lst)
    np_lst= np.array(lst)
    print("Nr:" + str(x))
    display_diff(np_lst)


names = []
f = open(r"C:\Users\horia\Desktop\Bank of America\codes.txt","r")
for line in f:
    names.append(line.split('\n'))
codes = []
for element in names:
    codes.append(element[0])

aux = []
code_to_index = {}
code_to_name = {}
name_to_code = {}
code_to_sector = {}
for i in range(0,90):
    aux += codes[i].split(' ')

for i in range(0,len(aux),3):
    code_to_index[aux[i]] = int(i/3)
    code_to_name[aux[i]] = aux[i+1]
    name_to_code[aux[i+1]] = aux[i]
    code_to_sector[aux[i]] = aux[i+2]
 # print(aux)
print()
print(code_to_name)
print()
print(name_to_code)
print()
print(code_to_sector)
print()
print(code_to_index)
print()
print(plot_graph("MSFT"))
print()
#plot_graph("RSW.L")
print(mean_volatility(["MSFT","T","FB","ORCL","CSCO","NVDA","MCRO.L"]))
