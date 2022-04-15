# 赛道巡线跟踪 - By: zyb - 周一 10月 25 2021
from uart import my_uart
# (11, 90, -34, 127, -128, 127)
grayLine = [(50, 100, -128, 127, -128, 127)]  # 用于巡线的阈值
err = 20  # 误差允许角度
grass = [(0, 21, 127, -128, -128, 16)]  # 黑色的阈值，二值化需反转


class LineDetect:
    def __init__(self):
        pass

    def line_track(self, img, grayLine=[(62, 100, -128, 127, -128, 127)], roi=(0, 20, 80, 40), err=5, type='default', angle_limit=20):
        """ 线性回归处理中线 """
        direct = 0
        angle_deg = 0

        img.binary(grayLine, invert=False)  # 二值化图像
        #self.line_width(img)
        line = img.get_regression(grayLine, roi=roi, robust=True)
        img.draw_line(0,roi[1],80,roi[1], color=127)
        img.draw_line(0,roi[3],80,roi[3], color=127)
        if line:
            if line.magnitude() > 8:
                if type=='grass' or 'turn':
                    err = 1
                direct, angle_deg = self.line_to_theta_and_dir(line, err=err)
                if type=='grass':
                    angle_err = 40-(line.x1()+line.x2())/2
                    angle_deg = int(angle_deg + angle_err/2)
                    if angle_deg < 0:
                        angle_deg = 0
                    if angle_deg > angle_limit:
                        angle_deg = angle_limit
                if type=='turn':
                    if (line.x1()+line.x2())/2 < 30: # 走到弯道内测，需要修正
                        direct = 1
                        angle_err = 40-(line.x1()+line.x2())/2
                        angle_deg = int(angle_deg + angle_err/2)
                        if angle_deg < 0:
                            angle_deg = 0
                        if angle_deg > angle_limit:
                            angle_deg = angle_limit
                my_uart.set_data(direct, 'direction')
                my_uart.set_data(angle_deg, 'angle')
                img.draw_line(line.line(), color=127)
                print('direct', direct)
                print('angle_deg', angle_deg)
                return direct, angle_deg

    def line_track_grass(self, img, grayLine=[(60, 100, -128, 127, -128, 127)], roi=(0, 20, 80, 40), err=1):
        """ 线性回归处理中线 """
        direct = 0
        angle_deg = 0

        img.binary([(0, 50, -47, -12, 0, 56)], invert=False)  # 二值化图像
        img.erode(1)
        line = img.get_regression(grayLine, roi=roi, robust=True)
        img.draw_line(0,roi[1],80,roi[1], color=127)
        img.draw_line(0,roi[3],80,roi[3], color=127)
        if line:
            if line.magnitude() > 8:
                direct, angle_deg = self.line_to_theta_and_dir(line, err=err)
                my_uart.set_data(direct, 'direction')
                my_uart.set_data(angle_deg, 'angle')
                img.draw_line(line.line(), color=127)
                angle_err = 40-(line.x1()+line.x2())/2
                angle_deg = int(angle_deg + angle_err/2)
                if angle_deg < 0:
                    angle_deg = 0
                if angle_deg > 30:
                    angle_deg = 30
                #print('direct', direct)
                #print('angle_deg', angle_deg)
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

    def line_width(self, img):
        #for l in img.find_lines(roi=(0,20,80,40),threshold = 1000, theta_margin = 25, rho_margin = 25):
            #if l.theta() > 75 and l.theta() < 105:
                #img.draw_line(l.line(), color = (255, 0, 0))
                #print(l.theta())
        for l in img.find_lines(roi=(20,0,40,20),threshold = 1000, theta_margin = 25, rho_margin = 25):
            if l.theta() < 15 or l.theta() > 165:
                img.draw_line(l.line(), color = (255, 0, 0))
                print(l)

my_line = LineDetect()
