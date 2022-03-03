# 主函数 - By: zyb - 周一 10月 25 2021
import sensor, image, time
import lineDef as LD
import data as DA
import pyb
from pyb import Pin, Timer, LED
from state_machine import Runway
"""    初始化openmv     """
LED(2).on()  # openmv启动标志
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
"""    变量定义   """
print("begin")
my_way = Runway()
print("now is state 1")
LED(2).off()  # openmv启动完成
"""    主循环    """
# TODO: 1. 测试重构后的bug；2. stm32 给 openmv 串口发送信息，形成闭环
while True:
    clock.tick()
    img = sensor.snapshot()
    """ ------颜色检测------- """
    # """
    my_way.state_exe(img)
    # """
    """ ------功能检测------ """
    # light.pulse_width_percent(1)
    # CD.colorSend(img, 'blue')
    # CD.colorSend(img, 'green')
    # CD.colorSend(img, 'yellow')
    # CD.colorSend(img, 'red')
    # CD.colorSend(img, 'brown')
    # light.pulse_width_percent(1) # 控制亮度 0~100
    # CD.ballRecog(img)
    """ ------赛道检测------ """
    # pyb.LED(1).on()
    # pyb.LED(2).on()
    # pyb.LED(3).on()
    # CD.ballRecog(img)
    # CD.colorSend(img, 'green')
    # LD.line_track(img.copy())
    # print(LD.line_track(img))
    """ ------数据发送------ """
    DA.sendData()
    DA.clearData()
    # print(clock.fps()) # 显示FPS
