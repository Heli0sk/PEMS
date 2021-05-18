import os
import xlrd
import pandas as pd
import numpy as np


if __name__ == '__main__':
    paths = './FF_data/flow/20-03-25_20-05-01/'
    num = 6
    l = os.listdir(paths)

    for vds in l:
        path=paths+'/'+str(vds)
        dfs = pd.read_excel(path + '/1.xlsx', index_col=None,header=None).values
        #print(dfs[0,:])
        for i in range(2, num + 1):
            df = pd.read_excel(path+ '/' + str(i) + '.xlsx', index_col=None).values
            dfs = np.row_stack((dfs, df))
        pd.DataFrame(dfs).to_excel(path + '/' + str(vds) + '_combine.xlsx', index=None, header=None)
        print(vds,'合并文件保存成功')












