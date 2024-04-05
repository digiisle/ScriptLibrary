import pandas as pd
import os
"""
使用python处理两个csv表
1、表1是用户表，包含字段有用户ID：teller_on，用户名：name，所属部门ID：branch_id；
2、表2是部门表，包含字段有部门ID：stru_id，部门名称：stru_fname，上级部门ID：sup_stru;
3、逻辑关系，表1和表2关联字段是branch_id--stru_id，用表1的branch_id在表2搜索可得到用户本部门名称，若sup_stru不为NULL，则表示有上级部门，再使用sup_stru在表2递归查询上级部门，直到sup_stru为空，表示已到顶级部门；
4、最终输出新表，新表包含字段有，用户ID：teller_on，用户名：name，完整部门：full_stru，部门之间用/分割；
"""

# 输入文件路径
user_table_file = input("请输入用户表文件路径：")
dept_table_file = input("请输入部门表文件路径：")

# 读取用户表和部门表
user_df = pd.read_csv(user_table_file)
dept_df = pd.read_csv(dept_table_file)

# 将部门表设置为字典，以便更快地查询
dept_dict = dict(zip(dept_df['stru_id'], dept_df['stru_fname']))

# 定义一个函数来递归查找完整部门名称
def find_full_department(dept_id):
    if pd.isnull(dept_id):
        return ""
    else:
        return find_full_department(dept_df.loc[dept_df['stru_id'] == dept_id, 'sup_stru'].iloc[0]) + "/" + dept_dict[dept_id]

# 应用函数并创建新的完整部门列
user_df['full_stru'] = user_df['branch_id'].apply(find_full_department)

# 去除最后一个部门后的斜杠
user_df['full_stru'] = user_df['full_stru'].str.rstrip('/')

# 输出文件路径
output_file = input("请输入输出文件路径：")

# 输出到新表，指定编码为UTF-8
user_df.to_csv(output_file, index=False, encoding='utf-8')




