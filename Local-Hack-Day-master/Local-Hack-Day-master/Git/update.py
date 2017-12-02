import csv
import pandas as pd
import pandas_datareader as web
import datetime as dt
import numpy as np

prices = csv.reader(open(r"C:\Users\horia\Desktop\prices.csv"))

def get_value(code):
    end = dt.datetime.now()
    start = end - dt.timedelta(days = 1)
    r = web.DataReader(code,'yahoo',start,end)
    return r.iloc[0,4]

matrix = [l for l in prices]
for i in range(1,32):
    for j in range(0,90):
        matrix[32-i][j] = matrix[32-i-1][j]

for i in range(0,90):
    matrix[1][i] = get_value(matrix[0][i])

writer = csv.writer(open(r"C:\Users\horia\Desktop\prices-v2.csv",'w'))
writer.writerows(matrix)
