# Untitled - By: 11374 - 周四 10月 21 2021
import image
import uartDef as UD
"""    颜色定义     """
color_threshold = {
    'black': {
        'threshold': [(1, 2, -2, -1, 0, 0)]
    },
    'brown': {
        'threshold': [(43, 68, -12, 16, 38, 62)]
    },
    'red': {
        'threshold': [(34, 66, 7, 42, -30, 11)]
    },
    'green': {
        'threshold': [(46, 72, -42, -12, -1, 57)]
    },
    'yellow': {
        'threshold': [(70, 83, -24, 8, 34, 74)]
    },
    'blue': {
        'threshold': [(45, 78, -28, 21, -32, -8)]
    }
}
black = 0
brown = 1
red = 2
green = 3
yellow = 4
blue = 5



def colorRecog(img, color, color_threshold):
    """颜色块识别

    Args:
        img : 待处理图像
        color (字符串): 期待识别的颜色
        color_threshold (字典): LAB阈值的字典
    """
    blobs = img.find_blobs(color_threshold[color]['threshold'],
                           merge=True,
                           pixels_threshold=25,
                           area_threshold=25,
                           margin=10)
    if (blobs):
        for blob in blobs:
            img.draw_rectangle(blob.rect())
            img.draw_string(blob.cx(),
                            blob.cy(),
                            color,
                            scale=1,
                            mono_space=False)
            UD.uartData(color)


def ballRecog(img, color, color_threshold):
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
        area = (c.x() - c.r(), c.y() - c.r(), 2 * c.r(), 2 * c.r())
        # area为识别到的圆的区域，即圆的外接矩形框
        statistics = img.get_statistics(roi=area)  # 像素颜色统计
        print(statistics)
        # (0,100,0,120,0,120)是红色的阈值，所以当区域内的众数（也就是最多的颜色），范围在这个阈值内，就说明是红色的圆。
        # l_mode()，a_mode()，b_mode()是L通道，A通道，B通道的众数。
        lab = color_threshold[color]['threshold']
        if lab[0] < statistics.l_mode(
        ) < lab[1] and lab[2] < statistics.a_mode() < lab[3] and lab[
                4] < statistics.b_mode() < lab[5]:  # if the circle is red
            img.draw_circle(c.x(), c.y(), c.r(),
                            color=(255, 0, 0))  # 识别到的红色圆形用红色的圆框出来
            print(getball)
            # 将非红色的圆用白色的矩形框出来

