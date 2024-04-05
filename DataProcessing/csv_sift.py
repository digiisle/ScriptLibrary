import pandas as pd
import os
"""
使用python处理两个csv表
1、表1是用户表，包含字段有用户ID：teller_on，用户名：name，所属部门ID：branch_id；
2、表2是部门表，包含字段有部门ID：stru_id，部门名称：stru_fname，上级部门ID：sup_stru;
3、逻辑关系，表1和表2关联字段是branch_id--stru_id，用表1的branch_id在表2搜索可得到用户本部门名称，若sup_stru不为NULL，则表示有上级部门，再使用sup_stru在表2递归查询上级部门，直到sup_stru为空，表示已到顶级部门；
4、最终输出新表，新表包含字段有，用户ID：teller_on，用户名：name，完整部门：full_stru，部门之间用/分割；
"""

# 读取部门表并构建部门字典
dept_table_file = input("请输入部门表文件路径：")
dept_df = pd.read_csv(dept_table_file)
dept_dict = dict(zip(dept_df['stru_id'], dept_df['stru_fname']))

# 定义一个函数来递归查找完整部门名称
def find_full_department(dept_id):
    full_department = ""
    while not pd.isnull(dept_id):
        full_department = "/" + dept_dict[dept_id] + full_department
        dept_id = dept_df.loc[dept_df['stru_id'] == dept_id, 'sup_stru'].iloc[0]
    return full_department.lstrip("/")

# 读取用户表的生成器
def read_user_chunks(filename, chunksize=10000):
    for chunk in pd.read_csv(filename, chunksize=chunksize):
        yield chunk

# 处理用户表数据
user_table_file = input("请输入用户表文件路径：")
output_file = input("请输入输出文件路径：")
chunksize = 10000  # 每次处理10000行数据
output_chunks = []

for user_chunk in read_user_chunks(user_table_file, chunksize=chunksize):
    user_chunk['full_stru'] = user_chunk['branch_id'].apply(find_full_department)
    output_chunks.append(user_chunk)

# 将处理后的数据写入输出文件
pd.concat(output_chunks).to_csv(output_file, index=False, encoding='utf-8')




