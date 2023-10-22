import os
import urllib.parse

import pandas as pd
import psycopg
from sqlalchemy import create_engine

filePath = os.path.abspath(r'D:\FunctionalTool\MyScripts\xlsx_csv_to_sql\File')

# 新建列表存放每个文件数据
newData = []

# 获取目录下所有文件
for dataInfo in os.listdir("D:\\FunctionalTool\\MyScripts\\xlsx_csv_to_sql\\File"):
    dataFile = os.path.join(filePath, dataInfo)
    print(dataFile)
    data = pd.read_excel(dataFile)
    data.head(2)

    # 删除不需要的行
    #data = data.drop(data.index[0:9])

    # 删除不需要的列
    data = data.drop(['认证时间','用户名','接入计算机名','IP','MAC','终端分组','端口','端口名称','SSID','认证状态','用户类型','详情','备注信息'], axis=1)
    
    # 合并重复行
    data = data.drop_duplicates()

    # 存入数据到newData
    newData.append(data)


# 合并每个文件数据后，再次合并重复行
data = pd.concat(newData)
data = data.drop_duplicates()

# 初始化数据库
param_dic = {
    "database": "********",
    "user": "********",
    "password": "********",
    "host": "********",
    "port": "5432"
}
dbschema = 'public'

connect ="postgresql+psycopg://%s:%s@%s:%s/%s" % (
    param_dic['user'],
    urllib.parse.quote_plus(param_dic['password']),
    param_dic['host'],
    param_dic['port'],
    param_dic['database']
)
engine = create_engine(connect, connect_args={
                       'options': '-csearch_path={}'.format(dbschema)})

# 将数据存储到MySQL数据库中
data.to_sql(name='BOSC_ALL_Switch', con=engine, schema=dbschema, index=True,
            index_label='ID', if_exists='append')

# 执行结束输出提示
print("Write to postgreSQL Successful!")
