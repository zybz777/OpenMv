# 主函数 - By: zyb - 周一 10月 25 2021
import sensor, image, time
# import data as DA
from pyb import Pin, Timer, LED
# user add
from color_detect import detect_black_obstacle, detect_blue_start_point
from ball_detect import detect_ball
from state import state_machine
from uart import my_uart
# from state_machine import Runway
"""    初始化openmv     """
LED(2).on()  # openmv启动标志
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
LED(2).off()  # openmv启动完成
clock = time.clock()
"""    主循环    """
while True:
    clock.tick()
    img = sensor.snapshot()
    """ ------状态机------- """
    state_machine.run(img)

    # 串口发送
    my_uart.send_data()
    my_uart.clear_data()
    # print(clock.fps())  # 显示FPS
