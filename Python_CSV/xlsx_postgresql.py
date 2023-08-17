import os
import urllib.parse

import pandas as pd
import psycopg2
from sqlalchemy import create_engine

filePath = os.path.abspath(r'D:\FunctionalTool\MyScripts\Python_CSV\File')

# 新建列表存放每个文件数据
newData = []

# 获取目录下所有csv文件
for csvInfo in os.listdir('D:\FunctionalTool\MyScripts\Python_CSV\File'):
    csvFile = os.path.join(filePath, csvInfo)
    print(csvFile)
    data = pd.read_excel(csvFile)
    data.head(2)

    # 删除不需要的列
    data = data.drop(['ID'], axis=1)
    
    # 合并重复行
    data = data.drop_duplicates()

    # 存入数据到newData
    newData.append(data)


# 合并每个文件数据后，再次合并重复行
data = pd.concat(newData)
data = data.drop_duplicates()

# 初始化数据库
param_dic = {
    "host": "pc.erickqian.top",
    "database": "superman_db",
    "user": "superman",
    "password": "245879@Qian."
}
dbschema = 'public'
connect = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (
    param_dic['user'],
    urllib.parse.quote_plus(param_dic['password']),
    param_dic['host'],
    param_dic['database']
)
engine = create_engine(connect, connect_args={
                       'options': '-csearch_path={}'.format(dbschema)})

# 将数据存储到MySQL数据库中
data.to_sql(name='T2WL_ALL_Session_No_SPort', con=engine, schema=dbschema, index=True,
            index_label='ID', if_exists='append')

# 执行结束输出提示
print("Write to postgreSQL Successful!")
