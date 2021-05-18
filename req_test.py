import time
import os
import numpy as np
import pandas as pd
import requests
import xlrd
import shutil
"""
下载PEMS源数据
1、更改下载数据的属性；
2、更改下载时间段；
final.csv 表中有需要下载的站点ID 
"""


def time_2_timestamp(input, lags=True):
    """默认True: 时间转化为时间戳, 包含时差计算"""
    if lags:
        timeArray = time.strptime(input, "%Y-%m-%d %H:%M")
        # 转换成时间戳
        return int(time.mktime(timeArray) + 8 * 60 * 60)  # 时差计算
    else:
        time_local = time.localtime(input - 8 * 60 * 60)
        return time.strftime("%Y-%m-%d %H:%M", time_local)


def download(save_path, vds, start_time, end_time):
    """时间转化为时间戳"""
    start_stamp, end_stamp = time_2_timestamp(start_time), time_2_timestamp(end_time)
    i = 1
    for begin in range(start_stamp, end_stamp, 60 * 60 * 24 * 7):
        url = get_url(vds, begin)
        down_load_data(save_path, url, i)
        i += 1
        f = xlrd.open_workbook(save_paths + "/1.xlsx", "rb")
        clowsname = f.sheet_by_name("Report Data").row_values(0)
        flag1 = False
        flag2 = False
        for itme in clowsname:
            if itme == "Flow (Veh/5 Minutes)":
            #if itme == "Speed (mph)":
                flag1 = True
        # for item in clowsname:
        #     if item == "Occupancy (%)":
        #         flag2=True
        if flag1 == True: #and flag2==True:
            continue
        else:
            raise("not flow!")
    print('OK')



def down_load_data(save_path, url, i):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    data = {"redirect": "", "username": "1397277295@qq.com",
            "password": "1=Ytopd2l", "login": "Login"}
    session = requests.session()

    response = session.post(url, headers=headers, data=data)
    response = session.get(url)
    #response1 = session.get("https://www.baidu.com")
    try:
        with open(save_path + '/' + str(i) + '.xlsx', 'wb') as f:
            f.write(response.content)
            print('下载成功')
    except IOError:
            print()


def get_url(vds, begin):
    str_begin = time_2_timestamp(begin, False)
    s_begin = str_begin[5:7] + '%2F' + str_begin[8:10] + '%2F' + str_begin[:4] + '+00%3A00'
    end = begin + 60 * 60 * 24 * 7 - 60
    str_end = time_2_timestamp(end, False)
    s_end = str_end[5:7] + '%2F' + str_end[8:10] + '%2F' + str_end[:4] + '+23%3A59'
    url = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=xls&station_id='+str(vds) + '&s_time_id=' + str(begin) + '&s_time_id_f=' + str(s_begin) + '&e_time_id=' + str(end) + '&e_time_id_f=' + str(s_end) + '&tod=all&tod_from=0&tod_to=0&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on'+'&q=flow&q2=&gn=5min&agg=on&lane1=on&lane2=on&lane3=on&lane4=on'
    # print(url)
    print('获取url: vds[%s] %s --- %s' % (str(vds), str_begin, str_end))
    print(url)
    return url


def combine_download_data(vds, path):
    num = len(os.listdir(path))
    dfs = pd.read_excel(path + '/1.xlsx', index_col=None).values
    for i in range(2, num + 1):
        df = pd.read_excel(path + '/' + str(i) + '.xlsx', index_col=None).values
        dfs = np.row_stack((dfs, df))
    pd.DataFrame(dfs).to_excel(path + '/' + str(vds) + '_combine.xlsx', index=None, header=None)
    print('合并文件保存成功')


if __name__ == '__main__':
    f = pd.read_csv("FF_ID_TSC.csv", sep=",").to_numpy()
    sta_id = f[:, 0]
    vds_list = []
    count=0
    for i in range(len(f)):
        vds_list.append(int(sta_id[i]))
    save_path = r'./FF_data/flow/'  # 文件保存路径
    # vds_list = [767523]  # 需要下载的VDS列表
    start_time, end_time = '2020-03-25 20:00', '2020-06-01 20:00'  # 数据下载开始于结束时间，每次下载一周，无数据则下载为空文件
    #for i in range(1000):
    for i in range(len(vds_list)):
        name = start_time[2:10] + '_' + end_time[2:10]
        save_paths = save_path + '/' + name + '/' + str(vds_list[i])  # 创建文件保存路径
        try:
            if not os.path.exists(save_paths):
                os.makedirs(save_paths)
            print('开始下载：%s   %s---%s' % (str(vds_list[i]), start_time, end_time))
            download(save_paths, vds_list[i], start_time, end_time)  # 下载文件
            combine_download_data(vds_list[i], save_paths)  # 将单个VDS下载文件进行合并
            print(save_paths)
            count+=1
            print(count)
            if count>=2000:
                break
            # if i==1076:
            #     break


            # f = xlrd.open_workbook(save_paths + "/1.xlsx", "rb")
            # clowsname = f.sheet_by_name("Report Data").row_values(0)
            # flag = False
            # for i in clowsname:
            #     if i == "Speed (mph)":
            #         flag = True
            #
            # if flag == True:
            #     print(count)
            #     count += 1
            # else:
            #     shutil.rmtree(save_paths)
        except Exception as e:
            f = open("log.txt", "a")
            logstr = str(vds_list[i]) + "," + str(e)
            shutil.rmtree(save_paths)
            f.write(logstr + "\n")
            f.close()
