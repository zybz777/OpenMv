# 赛道巡线跟踪 - By: zyb - 周一 10月 25 2021
from uart import my_uart
# (11, 90, -34, 127, -128, 127)
grayLine = [(40, 100, -34, 127, -128, 11)]  # 用于巡线的阈值
err = 20  # 误差允许角度
grass = [(0, 21, 127, -128, -128, 16)]  # 黑色的阈值，二值化需反转


class LineDetect:
    def __init__(self):
        pass

    def line_track(self, img, roi=(0, 10, 80, 40), err=20):
        """ 线性回归处理中线 """
        direct = 0
        angle_deg = 0

        img.binary(grayLine, invert=False)  # 二值化图像
        line = img.get_regression(grayLine, roi=roi,robust=True)

        if line:
            if line.magnitude() > 8:
                direct, angle_deg = self.line_to_theta_and_dir(line, err=err)
                my_uart.set_data(direct, 'direction')
                my_uart.set_data(angle_deg, 'angle')
                img.draw_line(line.line(), color=127)
                print('direct', direct)
                print('angle_deg', angle_deg)
                return direct, angle_deg

    def line_to_theta_and_dir(self, line, err=20):
        """ 计算中线角度 左1中0右-1 """
        angle = line.theta()
        angle_deg = 0
        direct = 0
        if line.theta() > 90:
            angle_deg = 180 - angle
            if angle_deg < err:
                direct = 0
            else:
                direct = 1  # 靠左
        elif line.theta() < 90:
            angle_deg = angle
            if angle_deg < err:
                direct = 0
            else:
                direct = 2  # 靠右
        return (direct, angle_deg)


my_line = LineDetect()
