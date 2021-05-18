import xlrd
import os
import shutil
import pandas as pd


node_num = 80

if __name__=="__main__":
    flow_path='./FF_data/flow/20-11-01_20-12-15/'
    occ_path='./FF_data/speed_and_occ/20-11-01_20-12-15/'
    f1=os.listdir(flow_path)
    f2=os.listdir(occ_path)
    list_id=[]
    #print(f1[0])
    cnt = 0
    for i in f1:
        if cnt >= node_num:
            break
        for j in f2:
            if cnt >= node_num:
                break
            if i==j:
                list_id.append(i)
                print("flow:",i,",occ and speed:",j)
                old_path1='./FF_data/flow/20-11-01_20-12-15/'+str(i)
                new_path1='./same_data/flow/same/'+str(i)
                shutil.copytree(old_path1,new_path1)
                old_path2='./FF_data/speed_and_occ/20-11-01_20-12-15/'+str(j)
                new_path2='./same_data/speed_and_occ/same/'+str(j)
                shutil.copytree(old_path2,new_path2)
                cnt += 1
    print(list_id)
    test=pd.DataFrame(data=list_id)
    test.to_csv('./ID_list3.csv',index=False,header=None)
    print(len(list_id))









