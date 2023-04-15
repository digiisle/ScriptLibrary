import random

My_Ball = []
while True:
    # 生成一位随机数
    Data = random.randint(1, 33)

    # 避免重复
    if Data not in My_Ball:
        # 把不重复的数字，添加到列表
        My_Ball.append(Data)

        # 返回6个不重复的红球
        if len(My_Ball) == 6:
            break

# 生成蓝球
My_Ball.sort()
Blue_Ball = random.randint(1, 16)
My_Ball.append(Blue_Ball)
print("本次号码:", My_Ball)
