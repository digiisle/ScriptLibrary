import base64

def encode():
    text = input("请输入要编码的文本: ")
    encoded_text = base64.b64encode(text.encode()).decode()
    print("Base64编码结果:", encoded_text)

def decode():
    encoded_text = input("请输入要解码的Base64字符串: ")
    decoded_text = base64.b64decode(encoded_text.encode()).decode()
    print("Base64解码结果:", decoded_text)

def main():
    while True:
        print("\n请选择操作:")
        print("1. 编码")
        print("2. 解码")
        print("3. 退出")
        choice = input("请输入选项数字: ")

        if choice == "1":
            encode()
        elif choice == "2":
            decode()
        elif choice == "3":
            print("谢谢使用！")
            break
        else:
            print("无效选项，请重新选择。")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已退出。")