import random
import signal
import sys


def GoodLuck(Num):
    for i in range(0,Num):
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
    return My_Ball


def quit(signum, frame):
    print("\nBye!")
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    print("""Welcome!\nCTRL+C退出程序\n输入格式: 仅限整数\n""")
    while True:
        Num = input("请输入随机数: ").replace(" ", "")
        if Num.isdigit(): 
            print("********************************************")
            Num=int(Num)
            print("本次号码:", GoodLuck(Num))
            print("********************************************\n")
        else:
            print("输入格式错误，请检查输入数字是否为整数!")
