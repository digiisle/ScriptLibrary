import os
import urllib.parse

import pandas as pd
from sqlalchemy import create_engine


filePath = os.path.abspath(r'D:\FunctionalTool\MyScripts\xlsx_csv_to_sql\File')

# 新建列表存放每个文件数据
newData = []

# 获取目录下所有csv文件
for dataInfo in os.listdir('D:\\FunctionalTool\\MyScripts\\xlsx_csv_to_sql\\File'):
    dataFile = os.path.join(filePath, dataInfo)
    print(dataFile)
    data = pd.read_csv(dataFile,encoding="gbk")
    data.head(2)

    # 删除不需要的列
    data = data.drop(['时间','时长(s)','虚拟系统','应用大类','应用小类','应用','带宽策略','总流量(Bytes)','正向流量(Bytes)',' 反向流量(Bytes)','源地区','源用户','源端口','目的地区'], axis=1)

    # 合并重复行
    data = data.drop_duplicates()

    # 存入数据到newData
    newData.append(data)


# 合并每个文件数据后，再次合并重复行
data = pd.concat(newData)
data = data.drop_duplicates()

# 初始化数据库
engine = create_engine('mysql+pymysql://superman:{password}@{host}:3306/{database}'.format(
    user='superman', password=urllib.parse.quote_plus("********"), host='********', database='********'), pool_recycle=1)

# 将数据存储到MySQL数据库中
data.to_sql('HW_Session_No_SPort', engine, index=True,
            index_label='ID', if_exists='append')

# 执行结束输出提示
print("Write to MySQL Successful!")
