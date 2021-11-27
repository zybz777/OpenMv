# 颜色相关定义 - By: zyb - 周一 10月 25 2021
# 缺点：没有封装成类，函数调用可能会混乱
import image
import data as DA
"""    颜色定义     """
color_threshold = {
    'black': {
        'threshold': [(1, 2, -2, -1, 0, 0)]
    },
    'brown': {
        'threshold': [(43, 60, -13, 16, 21, 62)]
    },
    'red': {
        'threshold': [(22, 60, 7, 42, -46, 11)]
    },
    'green': {
        'threshold': [(40, 76, -40, -17, 20, 40)]  # 阈值偏暗，在光线充足下识别不出
    },
    'yellow': {
        'threshold': [(54, 72, -26, -4, 17, 59)]
    },
    'blue': {
        'threshold': [(45, 78, -28, 21, -32, -8)]
    }
}

RedLab = color_threshold['red']['threshold'][0]
GreenLab = color_threshold['green']['threshold'][0]
BrownLab = color_threshold['brown']['threshold'][0]

# 定义颜色
black = 0
green = 1
red = 2
brown = 3
yellow = 4
blue = 5

ballColor = 0  # 球的颜色


def findMaxBlob(blobs):
    """ 寻找最大颜色块 """
    maxSize = 0
    for blob in blobs:
        nowSize = blob.w() * blob.h()
        if nowSize > maxSize:
            maxBlob = blob
            maxSize = nowSize
    return maxBlob


def colorRecog(img, color):
    ballSize = 0
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
                           pixels_threshold=1,
                           area_threshold=1,
                           margin=10)
    if blobs:
        blob = findMaxBlob(blobs)
        s = blob.w() * blob.h()  # 定义距离
        # 滤波操作 匹配赛道颜色块
        if color == 'blue' or color == 'red':
            s_max = 1500
            s_min = 100
            #print(s)
            ratio = blob.w() / blob.h()
            #print(ratio)
            if ratio < 3:
                return 0
        else:
            s_max = 20000
            s_min = 100
        # 滤波后输出结果
        if s_min < s and s < s_max:  # 绿色100
            img.draw_rectangle(blob.rect())
            img.draw_string(blob.cx(),
                            blob.cy(),
                            color,
                            scale=1,
                            mono_space=False)
            # print(color)
            return numColor  # 返回值为颜色编号


def colorSend(img, color):
    """ 识别颜色并发送数据 """
    global ballColor
    data1 = colorRecog(img, color)
    if data1 is not None:
        DA.setData(data1, 'color')
    # 状态复位 临近终点，准备再次录入小球
    if data1 == brown:
        ballColor = 0  # 球的颜色
    return data1


def ballColorRecog(img, color):
    ballSize = 0
    """ 用户快递球的颜色识别 """
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
                           pixels_threshold=1,
                           area_threshold=1,
                           margin=10)
    if blobs:
        blob = findMaxBlob(blobs)
        s = blob.w() * blob.h()  # 定义距离
        if s > 300:
            ballSize = round(blob.w() / blob.h(), 2)
            if 0.95 < ballSize and ballSize < 1.05:  # 滤波 过滤出长宽比为1的近似圆形
                img.draw_rectangle(blob.rect())
                img.draw_string(blob.cx(),
                                blob.cy(),
                                color,
                                scale=1,
                                mono_space=False)
                #print("color: {} size: {}".format(color, ballSize))
                # print(color)
                return numColor  # 返回值为颜色编号


def ballRecog(img):
    """ 结合颜色函数识别快递球，进行了滤波处理提高稳定性 """
    global ballColor
    g = r = b = 0
    for i in range(3):
        if ballColorRecog(img, 'green') == green:
            g += 1
        if ballColorRecog(img, 'red') == red:
            r += 1
        if ballColorRecog(img, 'brown') == brown:
            b += 1
    if g == 0 and r == 0 and b == 0:
        return
    if g >= b and g >= r:
        ballColor = green  # 判断为绿球
        DA.setData(1, 'ball')
        print("green ball")
    elif r >= g and r >= b:
        ballColor = red  # 判断为红球
        DA.setData(1, 'ball')
        print("red ball")
    elif b >= g and b >= r:
        ballColor = brown  # 判断为棕球
        DA.setData(1, 'ball')
        print("brown ball")


def ballColorMatch():
    """" 匹配现有球的颜色 """
    global ballColor
    if ballColor == green:
        DA.setData(1, 'isOpen')
    elif ballColor == red:
        DA.setData(1, 'isOpen')
    elif ballColor == brown:
        DA.setData(1, 'isOpen')
