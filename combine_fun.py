import pandas as pd
import numpy as np
import xlsxwriter
import xlrd
import xlwt
import os
from geopy.distance import geodesic


def count_dis_w(loc1, loc2):
    return geodesic(loc1, loc2).m


def fin_id(paths,types, nodes, times):
    f1_list = os.listdir(paths)
    final = open(str(types)+"_"+str(nodes)+"_"+str(times)+"_station_id.csv", "w+")
    for i in range(len(f1_list)):
        print(f1_list[i])
        final.write(str(f1_list[i]+",\n"))
    final.close()


def station_id_l(types, nodes, times):
    #sel_id = pd.read_csv("./"+str(types)+"_"+str(nodes)+"_"+str(times)+"_station_id.csv", header=None).to_numpy()[:, 0]
    sel_id = pd.read_csv("./ID_list333.csv",header=None).to_numpy()[:, 0]
    #print("./"+str(types)+"_"+str(nodes)+"_"+str(times)+"_station_id.csv")
    print("./ID_list33.csv")
    s_id_l = pd.read_csv("d07_text_meta_2019_03_23.txt", sep="\t").to_numpy()
    staionid_l = []
    for i in range(len(sel_id)):
        print(sel_id[i])
        id = int(sel_id[i])
        row = [int(id), ]
        j = 0
        for j in range(len(s_id_l)):
            if id == int(s_id_l[j][0]):
                break
        row.append(round(s_id_l[j][1], 6))
        row.append(round(s_id_l[j][2], 6))
        staionid_l.append(row)
    print(staionid_l)
    finalda = pd.DataFrame(np.array(staionid_l))
    finalda.to_csv("final_station_id_loc_"+str(types)+"_"+str(nodes)+"_"+str(times)+".csv", index=False)


# def csv_to_xl(paths):
#     folders_ls = os.listdir(paths)
#     for i in range(len(folders_ls)):
#         f = xlrd.open_workbook(paths + folders_ls[i] + "/" + '1.xlsx')
#         fda = f.sheet_by_name("Report Data")
#         title = fda.row(0)
#         csv = pd.read_csv(paths + folders_ls[i] + "/" + folders_ls[i] + '_combine.csv',
#                           encoding='utf-8', names=title)
#         csv.to_excel(paths + folders_ls[i] + "/" + folders_ls[i] + '_combine.xlsx',
#                      sheet_name='Report Data')


def combine_V(types, paths, nodes, times):
    final = pd.read_csv("final_station_id_loc_"+str(types)+"_"+str(nodes)+"_"+str(times)+".csv").to_numpy()
    o = xlsxwriter.Workbook("V_"+str(types)+"_"+str(times)+"_"+str(nodes)+".xlsx")
    o_sheet = o.add_worksheet("V_"+str(types)+str(times)+"_"+str(nodes))

    if types == "speed":
        limit_data = "Speed (mph)"
    elif types == "flow":
        limit_data = "Flow (Veh/5 Minutes)"
    else:
        limit_data = "Occupancy (%)"
    for i, ID in enumerate(final[:, 0]):
        print(ID)
        I = xlrd.open_workbook(paths + "/" +str(int(ID))+ "/" + str(int(ID)) + "_combine.xlsx", "rb")
        j = 0
        table=I.sheet_by_name("Sheet1")
        n=table.ncols
        for j in range(1, n):
            #print(I.sheet_by_name("Sheet1").col_values(j)[0])
            if I.sheet_by_name("Sheet1").col_values(j)[0] == limit_data:
                #print(I.sheet_by_name("Sheet1").col_values(j)[0])
                break
        list_v = np.array(I.sheet_by_name("Sheet1").col_values(j)[1:-1])
        print(ID, list_v)
        for rows, itemt in enumerate(list_v):
            o_sheet.write(rows, i, itemt)
            # else:
            #     x_temp = int((list_v[t - 1] + list_v[t - 2] + list_v[t - 3] + list_v[t - 4] + list_v[t - 5]) / 5) + 1
            #     # x_temp = (Y_Max - Y_Min) * ((x_temp - X_Min) / (X_MAX - X_Min)) + Y_Min
            #     o_sheet.write(t, i, int(x_temp) + 1)
    o.close()


def combine_w(nodes, types, times):
    matax = []
    loc_s = pd.read_csv("final_station_id_loc_"+str(types)+"_"+str(nodes)+"_"+str(times)+".csv").to_numpy()
    for i in loc_s:
        row = []
        for j in loc_s:
            temp = count_dis_w(i[1:], j[1:])
            row.append(temp)
        matax.append(row)
    w = np.array(matax).reshape([nodes, nodes])
    f = open("w_"+str(nodes)+".csv", "w+")
    for i in range(nodes):
        for j in range(nodes):
            if j == nodes:
                f.write(str(w[i][j]))
            else:
                f.write(str(w[i][j]) + ",")
        f.write("\n")
    f.close()


if __name__ == "__main__":
    # dataPath = "./same_data/speed_and_occ/same"
    dataPath = "./FF_data/flow/20-03-25_20-05-01"
    time = "20-03-25_20-05-01"
    types = "flow"
    nodes = 116
    # del_bad_data()
    fin_id(dataPath, types, nodes, time)
    station_id_l(types, nodes, time)
    # csv_to_xl(dataPath)
    combine_V(types, dataPath, nodes, time)
    combine_w(nodes, types, time)
