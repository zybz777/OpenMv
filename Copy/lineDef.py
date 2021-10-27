# 赛道巡线跟踪 - By: 11374 - 周一 10月 25 2021
import data as DA

grayLine = (63, 100, -128, 127, -128, 127)  # 用于巡线的阈值
err = 5  # 误差允许角度


def line_to_theta_and_dir(line):
    """计算中线角度 左1中0右-1

    Args:
        line ([type]): 线性回归得到的中线

    Returns:
        (int, int): 方向，角度
    """
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


def line_track(img, track_color):
    """线性回归处理中线

    Args:
        img : 待处理图像
        track_color : 追踪颜色阈值，彩色域下为白色的6位LAB阈值

    Returns:
        (int, int): 方向，角度
    """
    direct = 0
    angle_deg = 0

    img.binary([(42, 255)])  # 二值化图像
    img.crop([0, 15, 80, 60])  # 滤波
    img.erode(1)  # 滤波

    line = img.get_regression([track_color], robust=True)

    img.draw_line(line.line(), color=127)
    if line.magnitude() > 8:
        direct, angle_deg = line_to_theta_and_dir(line)
        DA.direction = direct # 将数据传出，准备发送给主控
        DA.angle = angle_deg # 将数据传出，准备发送给主控
        return direct, angle_deg
