# 颜色相关定义 - By: zyb - 周一 10月 25 2021
import image
import data as DA
"""    颜色定义     """
color_threshold = {
    'black': {
        'threshold': [(1, 2, -2, -1, 0, 0)]
    },
    'brown': {
        'threshold': [(43, 60, -12, 16, 38, 62)]
    },
    'red': {
        'threshold': [(34, 66, 7, 42, -30, 11)]
    },
    'green': {
        'threshold': [(36, 64, -40, -17, 23, 49)]
    },
    'yellow': {
        'threshold': [(70, 83, -24, 8, 34, 74)]
    },
    'blue': {
        'threshold': [(45, 78, -28, 21, -32, -8)]
    }
}

RedLab = color_threshold['red']['threshold']
GreenLab = color_threshold['green']['threshold']
BrownLab = color_threshold['brown']['threshold']

# 定义颜色
black = 0
green = 1
red = 2
brown = 3
yellow = 4
blue = 5

ballColor = 0  # 记录快递球的颜色


def findMaxBlob(blobs):
    """ 寻找最大颜色块 """
    maxSize = 0
    for blob in blobs:
        nowSize = blob.w() * blob.h()
        if nowSize > maxSize:
            maxBlob = blob
            maxSize = nowSize
    return maxBlob


def findMaxCircle(circles):
    """ 寻找最大圆形 """
    maxSize = 0
    for circle in circles:
        nowSize = circle.r()
        if nowSize > maxSize:
            maxCircle = circle
            maxSize = nowSize
    return maxCircle


def colorRecog(img, color):
    """ 颜色块识别 """
    numColor = 0
    # 匹配一下输入的color是什么颜色
    if color == 'black':
        numColor = black
    elif color == 'green':
        numColor = green
    elif color == 'red':
        numColor = red
    elif color == 'brown':
        numColor = brown
    elif color == 'yellow':
        numColor = yellow
    elif color == 'blue':
        numColor = blue
    # 颜色匹配
    blobs = img.find_blobs(color_threshold[color]['threshold'],
                           merge=True,
                           pixels_threshold=30,
                           area_threshold=30,
                           margin=10)
    if blobs:
        blob = findMaxBlob(blobs)
        s = (blob.w() + blob.h()) / 2  # 定义距离
        if s > 20:
            img.draw_rectangle(blob.rect())
            img.draw_string(blob.cx(),
                            blob.cy(),
                            color,
                            scale=1,
                            mono_space=False)
            print(color)
            DA.color = numColor  # 将数据传出，准备发送给主控


def ballRecog(img):
    """ 识别快递球 """
    circles = img.find_circles(threshold=3500,
                               x_margin=10,
                               y_margin=10,
                               r_margin=10,
                               r_min=2,
                               r_max=100,
                               r_step=2)
    if circles:
        c = findMaxCircle(circles)
        area = (c.x() - c.r(), c.y() - c.r(), 2 * c.r(), 2 * c.r())  # area为识别到的圆的区域，即圆的外接矩形框
        img.draw_circle(c.x(), c.y(), c.r())
        
        statistics = img.get_statistics(roi=area)  # 像素颜色统计
        print(statistics)

        # 判断是否红球
        if RedLab[0] < statistics.l_mode() < RedLab[1] and RedLab[2] < statistics.a_mode() < RedLab[3] and RedLab[4] < statistics.b_mode() < RedLab[5]:
            print("getREDBall")
            ballColor = red  # 用于下次颜色识别时的判断是否抛出球
        # 判断是否绿球
        elif GreenLab[0] < statistics.l_mode() < GreenLab[1] and GreenLab[2] < statistics.a_mode() < GreenLab[3] and GreenLab[4] < statistics.b_mode() < GreenLab[5]:
            print("getGREENball")
            ballColor = green  # 用于下次颜色识别时的判断是否抛出球
        # 判断是否棕球
        elif BrownLab[0] < statistics.l_mode() < BrownLab[1] and BrownLab[2] < statistics.a_mode() < BrownLab[3] and BrownLab[4] < statistics.b_mode() < BrownLab[5]:
            print("getBROWNball")
            ballColor = brown  # 用于下次颜色识别时的判断是否抛出球


def ballColorMatch(img):
    """" 匹配现有球的颜色 """
    if ballColor == green:
        colorRecog(img, 'green')
        ballColor = 0  # 本次循环送球完毕
        DA.isOpen = 1  # 传出数据
    elif ballColor == red:
        colorRecog(img, 'red')
        ballColor = 0  # 本次循环送球完毕
        DA.isOpen = 1  # 传出数据
    elif ballColor == brown:
        colorRecog(img, 'brown')
        ballColor = 0  # 本次循环送球完毕
        DA.isOpen = 1  # 传出数据

