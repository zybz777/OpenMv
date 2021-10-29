# 主函数 - By: zyb - 周一 10月 25 2021
import sensor, image, time
import colorDef as CD
import lineDef as LD
import data as DA
"""    初始化openmv     """
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
"""    主循环    """
while True:
    clock.tick()
    img = sensor.snapshot()
    """ ------小球判断------ """
    if CD.ballColor == 0:
        CD.ballRecog(img)
    else:
        CD.ballColorMatch(img)  # 匹配开舱门的颜色位置
    """ ------颜色检测------- """
    CD.colorSend(img, 'blue')
    CD.colorSend(img, 'brown')
    CD.colorSend(img, 'red')
    CD.colorSend(img, 'green')
    CD.colorSend(img, 'yellow')
    CD.colorSend(img, 'blue')
    """ ------赛道检测------ """
    LD.line_track(img.copy())
    # print(LD.line_track(img))
    """ ------数据发送------ """
    DA.sendData()
    DA.clearData()
    print(clock.fps())
