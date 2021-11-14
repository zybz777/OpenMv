# Untitled - By: 11374 - 周日 11月 14 2021

import sensor, image, time
enable_lens_corr = False # 获得更直的线
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
stairs_thresold = [(72, 100, -128, 127, -128, 127)]


def find_cloest_line(lines):
    max_line_pos = 0
    res = None
    for l in lines:
        if (85 <= l.theta()) and (l.theta() <= 95):
            temp = (l.y1() + l.y2()) / 2
            if temp > max_line_pos:
                max_line_pos = temp
                res = l
    return res


while(True):
    clock.tick()
    img = sensor.snapshot()
    img.binary(stairs_thresold, invert=True)  # 二值化图像
   # img.crop([0, 15, 80, 60])  # 滤波
    img.erode(1)  # 滤波
    if enable_lens_corr: img.lens_corr(1.2)
    #for l in img.find_lines(threshold = 3000, theta_margin = 25, rho_margin = 25):
        #if (85 <= l.theta()) and (l.theta() <= 95):
            #print('the line y1:{}, y2:{}'.format(l.y1(),l.y2()))
            #img.draw_line(l.line(), color = (255, 0, 0))
    lines = img.find_lines(threshold = 3000, theta_margin = 25, rho_margin = 25)
    l = find_cloest_line(lines)
    if l is not None:
        img.draw_line(l.line(), color = (255, 0, 0))
        # print(l)
    #print(clock.fps())
