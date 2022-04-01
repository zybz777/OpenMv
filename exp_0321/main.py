# 主函数 - By: zyb - 周一 10月 25 2021
import sensor, image, time
from pyb import Pin, Timer, LED
# user add
from color_detect import detect_black_obstacle, detect_blue_start_point, detect_user
from ball_detect import detect_ball
from line_detect import my_line
from state import state_machine
from uart import my_uart
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
    state_machine.state_machine_exe(img)
    #my_line.line_track(img)
    #my_uart.send_data()
    #my_uart.clear_data()
    #state_machine.find_user(img, 1)
    #state_machine.find_yellow_upstair(img)
    #detect_user(img, 3)
    #LED(2).on()A
    #print(clock.fps())  # 显示FPS
