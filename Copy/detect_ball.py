import image
import data as DA
from utils import color_type, color_threshold, find_max_blob


class Ball():
    def __init__(self):
        self.color_type = None

    
def ball_Color_Recog(img, color):
    ballSize = 0
    """ 用户快递球的单独颜色识别 """
    color_num = color_type[color]  # 匹配color
    # 颜色匹配
    blobs = img.find_blobs(color_threshold[color]['threshold'],
                           merge=True,
                           pixels_threshold=1,
                           area_threshold=1,
                           margin=10)
    if blobs:
        blob = find_max_blob(blobs)
        if blob.w() * blob.h() > 300:  # 滤除微小干扰
            ballSize = round(blob.w() / blob.h(), 2)
            if 0.95 < ballSize and ballSize < 1.05:  # 滤波 过滤出长宽比为1的近似圆形
                img.draw_rectangle(blob.rect())
                img.draw_string(blob.cx(),
                                blob.cy(),
                                color,
                                scale=1,
                                mono_space=False)
                # print("color: {} size: {}".format(color, ballSize))
                # print(color)
                return color_num  # 返回值为颜色编号
