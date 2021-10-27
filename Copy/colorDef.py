# Untitled - By: 11374 - 周四 10月 21 2021
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
# 定义颜色
black = 0
green = 1
red = 2
brown = 3
yellow = 4
blue = 5

ballColor = 0 #记录快递球的颜色

def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob

def colorRecog(img, strColor, numColor, color_threshold):
    """颜色块识别

    Args:
        img : 待处理图像
        color (字符串): 期待识别的颜色
        color_threshold (字典): LAB阈值的字典
    """
    blobs = img.find_blobs(color_threshold[strColor]['threshold'],
                           merge=True,
                           pixels_threshold=30,
                           area_threshold=30,
                           margin=10)
    if (blobs):
        blob = find_max(blobs)
        s = (blob.w()+blob.h())/2 # 定义距离
        if s > 13:
            img.draw_rectangle(blob.rect())
            img.draw_string(blob.cx(),
                            blob.cy(),
                            strColor,
                            scale=1,
                            mono_space=False)
            print(strColor)
            DA.color = numColor # 将数据传出，准备发送给主控


def ballRecog(img, color_threshold):
    """识别快递球

    Args:
        img : 待处理图像
        color (字符串): 期待识别的颜色
        color_threshold (字典): LAB阈值的字典
    """
    for c in img.find_circles(threshold=3500,
                              x_margin=10,
                              y_margin=10,
                              r_margin=10,
                              r_min=2,
                              r_max=100,
                              r_step=2):
        area = (c.x() - c.r(), c.y() - c.r(), 2 * c.r(), 2 * c.r()
                )  # area为识别到的圆的区域，即圆的外接矩形框

        statistics = img.get_statistics(roi=area)  # 像素颜色统计
        print(statistics)
        # 判断是否红球
        lab1 = color_threshold['red']['threshold']
        if lab1[0] < statistics.l_mode(
        ) < lab1[1] and lab1[2] < statistics.a_mode() < lab1[3] and lab1[
                4] < statistics.b_mode() < lab1[5]:
            img.draw_circle(c.x(), c.y(), c.r())
            print("getREDBall")
            ballColor = red # 用于下次颜色识别时的判断是否抛出球
        # 判断是否绿球
        lab2 = color_threshold['green']['threshold']
        if lab2[0] < statistics.l_mode(
        ) < lab2[1] and lab2[2] < statistics.a_mode() < lab2[3] and lab2[
                4] < statistics.b_mode() < lab2[5]:
            img.draw_circle(c.x(), c.y(), c.r())
            print("getGREENball")
            ballColor = green # 用于下次颜色识别时的判断是否抛出球
        # 判断是否棕球
        lab3 = color_threshold['brown']['threshold']
        if lab3[0] < statistics.l_mode(
        ) < lab3[1] and lab3[2] < statistics.a_mode() < lab3[3] and lab3[
                4] < statistics.b_mode() < lab3[5]:
            img.draw_circle(c.x(), c.y(), c.r())
            print("getBROWNball")
            ballColor = brown # 用于下次颜色识别时的判断是否抛出球

