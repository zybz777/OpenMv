"""重构 球类 - By: zyb - 周日 2月 13 2022
"""
import image
from data import set_data
from utils import color_type, color_threshold, find_max_blob


class Detect_ball():
    def __init__(self):
        self.color_type = None
        self.exists = False

    def judge_ball_color(self, img, color_input):
        """判断小球颜色

        Args:
            img (img): 该帧图像
            color_input (str): 待识别颜色

        Returns:
            Bool: True of Flase
        """
        # 颜色匹配
        blobs = img.find_blobs(color_threshold[color_input]['threshold'],
                               merge=True,
                               pixels_threshold=1,
                               area_threshold=1,
                               margin=10)

        if blobs is None:
            return False
        blob = find_max_blob(blobs)
        if blob is None:
            return False
        s = blob.w() * blob.h()  # 定义大小
        if s < 300:
            return False

        ratio = round(blob.w() / blob.h(), 2)
        if 0.95 < ratio and ratio < 1.05:  # 滤波 过滤出长宽比为1的近似圆形
            img.draw_rectangle(blob.rect())
            img.draw_string(blob.cx(),
                            blob.cy(),
                            color_input,
                            scale=1,
                            mono_space=False)
            # print("color: {} size: {}".format(color, ratio))
            # print(color)
            return True  # 返回值为颜色编号
        else:
            return False

    def detect_ball(self, img):
        """判断图像中球及其颜色

        Args:
            img (img): 该帧图像

        Returns:
            Bool: True or False 是否识别到小球
        """
        g = r = b = 0
        for i in range(3):
            if self.judge_ball_color(img, 'green') is True:
                g += 1
            elif self.judge_ball_color(img, 'red') is True:
                r += 1
            elif self.judge_ball_color(img, 'brown') is True:
                b += 1
            else:
                continue
        if g == 0 and r == 0 and b == 0:
            return False

        if g >= b and g >= r:
            self.color_type = color_type["green"]  # 判断为绿球
            self.exists = True
            set_data(1, 'ball') # 写入串口数据
            print("green ball")
            return True
        elif r >= g and r >= b:
            self.color_type = color_type["red"]  # 判断为红球
            self.exists = True
            set_data(1, 'ball')
            print("red ball")
            return True
        elif b >= g and b >= r:
            self.color_type = color_type["brown"]  # 判断为棕球
            self.exists = True
            set_data(1, 'ball')
            print("brown ball")
            return True
        else:
            self.color_type = None  # 判断失败
            self.exists = False
            return False

    def send_ball(self):
        """判断球是否需要发射
        """
        if self.color_type == color_type["green"]:
            set_data(1, 'isOpen')
            self.ball_reset()
        elif self.color_type == color_type["red"]:
            set_data(1, 'isOpen')
            self.ball_reset()
        elif self.color_type == color_type["brown"]:
            set_data(1, 'isOpen')
            self.ball_reset()

    def ball_reset(self):
        """重置对象内数据
        """
        self.color_type = None
        self.exists = False
