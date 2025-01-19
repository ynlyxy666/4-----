import re

def dec2hex(dec):
    return hex(dec)[2:]

if __name__ == "__main__":
    a = input("请输入三个用空格分隔的RGB值\n格式：255 255 255\n>")
    # 检查输入格式是否为三个用空格分隔的数字
    if not re.match(r"\d{1,3}\s\d{1,3}\s\d{1,3}", a):
        print("输入格式错误，请重新输入。")
        exit(1)

    # 提取RGB数组中的三个数值并转换为元组
    r, g, b = map(int, a.split())
    rgb_tuple = (r, g, b)

    # 检查三个数值是否均小于255
    if r > 255 or g > 255 or b > 255:
        print("输入的RGB值必须小于255，请重新输入。")
        exit(1)

    # 将RGB值转换为十六进制
    r_hex = dec2hex(r).zfill(2)
    g_hex = dec2hex(g).zfill(2)
    b_hex = dec2hex(b).zfill(2)

    # 输出十六进制数
    print('结果：\n','#',r_hex, g_hex, b_hex,sep='')