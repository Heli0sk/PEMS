import numpy as np
import pandas as pd

import xlsxwriter
import xlrd
import os


# paths = r"E:\PycharmProject\PEMS\FF_data\flow\19-03-25_19-05-01"
# files = os.listdir(paths)
# print(files)
# print(len(files))
# files = list(map(int, files))
# data = pd.DataFrame(data=files)
# data.to_csv('./ID_list33.csv', index=False, header=None)
# # print(data.head())
# # print("="*55)
# list3 = pd.read_csv("./ID_list33.csv")
# print(list3.head())


# 保留 FR ML OR
# data = pd.read_csv("FF_ID3.csv", sep=",")
# print(data.head())
# print(data.shape)
# data = data[(data['Type'] == 'FR') | (data['Type'] == 'ML') | (data['Type'] == 'OR')]
# print(data.shape)
# data.to_csv('./FF_ID_TSC2.csv', index=False)


start_time, end_time = '2020-03-25 20:00', '2020-06-01 20:00'
save_path = r'./FF_data/flow/'
name = start_time[2:10] + '_' + end_time[2:10]
save_paths = save_path + '/' + name + '/' + str(715927)
f = xlrd.open_workbook(save_paths + "/1.xlsx", "rb")
