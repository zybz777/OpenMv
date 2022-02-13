"""重构 赛道颜色检测类 - By: zyb - 周日 2月 13 2022
"""
import image
from data import setData
from utils import color_type, color_threshold, find_max_blob


class Detect_color():
    """ 检测是否存在该种颜色 """
    def __init__(self):
        self.color_type = None  # 最后结果展示
        self.color_exist = False  # 是否检测到颜色

    def judge_choose_color(self, img, color_input):
        """ 判断指定颜色
        成功，返回 颜色编号, True
        失败，返回 None, False
        """
        self.color_type = color_type[color_input]  # 接收输入
        blobs = img.find_blobs(color_threshold[color_input]['threshold'],
                               merge=True,
                               pixels_threshold=1,
                               area_threshold=1,
                               margin=10)  # 搜索输入色块
        if blobs is None:
            self.color_type = None
            self.color_exist = False
            return self.color_type, self.color_exist  # 失败退出

        # 颜色提取
        blob = find_max_blob(blobs)  # 最大色块
        s = blob.w() * blob.h()  # 距离依据
        # 滤波操作 匹配赛道颜色块
        if color_input == 'blue' or color_input == 'red' or color_input == 'yellow':
            s_max = 1500
            s_min = 100
            # print(s)
            ratio = blob.w() / blob.h()
            # print(ratio)
            if ratio < 3:
                self.color_type = None
                self.color_exist = False
                return self.color_type, self.color_exist  # 失败退出
        else:
            s_max = 20000
            s_min = 100
        # 滤波后输出结果
        if s_min < s and s < s_max:  # 绿色100
            img.draw_rectangle(blob.rect())
            img.draw_string(blob.cx(),
                            blob.cy(),
                            color_input,
                            scale=1,
                            mono_space=False)
            # print(color_input)
            self.color_type = color_type[color_input]
            self.color_exist = True
            return self.color_type, self.color_exist  # 成功判断

    def color_send(self, img, color_input):
        """ 识别颜色并发送数据 
            成功, 返回True
            失败，返回False
        """
        self.judge_choose_color(img, color_input)
        if self.color_exist:
            setData(self.color_type, 'color')
            self.color_reset()
            return True
        else:
            self.color_reset()
            return False

    def color_reset(self):
        self.color_type = None  # reset
        self.color_exist = False  #
        # 状态复位 临近终点，准备再次录入小球
        # if data1 == brown:
        #     ballColor = 0  # 球的颜色
        # return data1
