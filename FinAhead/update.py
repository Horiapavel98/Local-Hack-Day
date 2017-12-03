import csv
import pandas as pd
import pandas_datareader as web
import datetime as dt
import numpy as np



def get_value(code):
    end = dt.datetime.now()
    start = end - dt.timedelta(days = 1)
    r = web.DataReader(code,'yahoo',start,end)
    return r.iloc[0,4]

def update_csv(start_file, end_file):
    prices = csv.reader(open(start_file)) # start_file - the path of the file you want to process

    matrix = [l for l in prices]
    for i in range(29, 0, -1):
        for j in range(0, 90):
            matrix[i+1][j] = matrix[i][j]

    for x in range(0,90):
        try:
            matrix[1][x] = get_value(matrix[0][x])
        except:
            matrix[1][x] = ''
        print("I just did: " + str(x))

    writer = csv.writer(open(end_file,'w')) # end_file - the path of the file you wanna create'
    writer.writerows(matrix)


#print("I finished !!")
