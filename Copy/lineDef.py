# 赛道巡线跟踪 - By: zyb - 周一 10月 25 2021
import data as DA

grayLine = [(63, 100, -128, 127, -128, 127)]  # 用于巡线的阈值
err = 5  # 误差允许角度


def line_to_theta_and_dir(line):
    """ 计算中线角度 左1中0右-1 """
    angle = line.theta()
    angle_deg = 0
    direct = 0
    if line.theta() > 90:
        angle_deg = 180 - angle
        if line.theta() < err:
            direct = 0
        else:
            direct = 1  # 靠左
    elif line.theta() < 90:
        angle_deg = angle
        if line.theta() < err:
            direct = 0
        else:
            direct = -1  # 靠右
    return (direct, angle_deg)


def line_track(img):
    """ 线性回归处理中线 """
    direct = 0
    angle_deg = 0

    img.binary([(42, 255)])  # 二值化图像
    img.crop([0, 15, 80, 60])  # 滤波
    img.erode(1)  # 滤波

    line = img.get_regression(grayLine, robust=True)

    if line:
        img.draw_line(line.line(), color=127)
        if line.magnitude() > 8:
            direct, angle_deg = line_to_theta_and_dir(line)
            DA.setData(direct, 'direction')
            DA.setData(angle_deg, 'angle')
            return direct, angle_deg
