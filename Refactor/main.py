# 主函数 - By: zyb - 周一 10月 25 2021
import sensor, image, time
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
    """ ------状态机------- """
    # my_way.state_exe(img)  # 颜色信息
    # my_way.line_track(img.copy())
    """ ------测试------ """
    # my_way.my_ball.detect_ball(img)
    # my_way.my_color.color_send(img, 'green')
    """ ------数据发送------ """
    DA.send_data()
    DA.clear_data()
    # print(clock.fps()) # 显示FPS
