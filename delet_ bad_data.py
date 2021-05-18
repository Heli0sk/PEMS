import os
import xlrd
import shutil


def find_id(paths, types, ID):
    I = xlrd.open_workbook(paths + str(int(ID)) + "/" + str(int(ID)) + "_combine.xlsx", "rb")
    if types == "speed":
        limit_data = "text:'Speed (mph)'"

    elif types == "flow":
        limit_data = "text:'Flow (Veh/5 Minutes)'"

    else:
        limit_data = "text:'Occupancy (%)'"
    table = I.sheet_by_name("Sheet1")
    n = table.ncols
    for j in range(1, n):
        if I.sheet_by_name("Sheet1").col_values(j)[0] == limit_data:
            break
    valus = I.sheet_by_name("Sheet1").col_values(j)[1:-1]
    if set(valus) == {0}:
        shutil.rmtree(paths+str(int(ID))+"/")


if __name__ == "__main__":
    paths = "./FF_data/flow/20-03-25_20-05-01/"
    ID_list = os.listdir(paths)
    for i in ID_list:
        find_id(paths, "flow", i)
        print(i)
