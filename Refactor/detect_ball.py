"""重构 球类 - By: zyb - 周日 2月 13 2022
"""
import image
from data import setData
from utils import color_type, color_threshold, find_max_blob


class Ball():
    def __init__(self):
        self.color_type = None
        self.exists = False

    def judge_ball_color(self, img, color_input):
        """ 底层函数， 球的颜色判断 
        成功, True
        失败, False
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
        """ 上层接口，检测球的颜色 
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
            return None
        if g >= b and g >= r:
            self.color_type = color_type["green"]  # 判断为绿球
            self.exists = True
            setData(1, 'ball')
            print("green ball")
        elif r >= g and r >= b:
            self.color_type = color_type["red"]  # 判断为红球
            self.exists = True
            setData(1, 'ball')
            print("red ball")
        elif b >= g and b >= r:
            self.color_type = color_type["brown"]  # 判断为棕球
            self.exists = True
            setData(1, 'ball')
            print("brown ball")
        else:
            self.color_type = None  # 判断失败
            self.exists = False

    def send_ball(self):
        """" 上层接口，发送球，reset该类 """
        if self.color_type == color_type["green"]:
            setData(1, 'isOpen')
            self.ball_reset()
        elif self.color_type == color_type["red"]:
            setData(1, 'isOpen')
            self.ball_reset()
        elif self.color_type == color_type["brown"]:
            setData(1, 'isOpen')
            self.ball_reset()

    def ball_reset(self):
        self.color_type = None
        self.exists = False
