"""重构 赛道状态机类 - By: zyb - 周日 2月 13 2022
"""
from detect_ball import Detect_ball
from detect_color import Detect_color
from detect_line import Detect_line
from utils import statesets, color_type
from pyb import Pin, Timer, LED
import time
from data import reveive_data

flag_grass = 0
sleep_time = 2  # 全局延迟时间，每个状态切换之间给狗子行走的时间，防止将当前颜色识别成下一状态颜色
"""   补光版定义   """
light = Timer(2,
              freq=50000).channel(1, Timer.PWM,
                                  pin=Pin("P6"))  # 50kHz pin6 timer2 channel1
light.pulse_width_percent(0)  # 控制亮度 0~100


class Runway():
    def __init__(self):
        self.current_state = statesets["state_1_start"]
        self.my_ball = Detect_ball()  # 检测球
        self.my_color = Detect_color()  # 检测颜色
        self.my_line = Detect_line()  # 检测中线

    def state_exe(self, img):
        """状态机执行

        Args:
            img (img): 每一帧图像
        """
        global count, flag_grass
        # state 1
        if self.current_state == statesets["state_1_start"]:

            if self.my_color.color_send(img, 'blue') is True:  # 识别蓝色成功
                self.state_trans()  # 状态转移

        # state 2
        elif self.current_state == statesets["state_2_load"]:

            if self.my_ball.detect_ball(img) is True:  # 识别小球成功
                self.state_trans()

        # state 3
        elif self.current_state == statesets["state_3_user1"]:

            if self.my_color.color_send(img, 'green') is True:  # 识别绿色成功，用户1
                if self.my_ball.color_type == color_type["green"]:  # 匹配成功
                    self.my_ball.send_ball()  # 开舱门并reset
                self.state_trans()  # 状态转移

        # state 4
        elif self.current_state == statesets["state_4_stair"]:

            if self.my_color.color_send(img, 'yellow') is True:  # 识别黄色成功，上楼梯
                self.state_trans()

        # state 5
        elif self.current_state == statesets["state_5_user2"]:

            if self.my_color.color_send(img, 'red'):  # 识别红色成功，用户2
                if self.my_ball.color_type == color_type["red"]:
                    self.my_ball.send_ball()  # 匹配开舱门并reset
                self.state_trans()

        # state 6
        elif self.current_state == statesets["state_6_grass"]:

            if flag_grass == 0 and self.my_color.color_send(img,
                                                            'green') is True:
                flag_grass = 1
            elif flag_grass == 1 and self.my_color.color_send(
                    img, 'green') is False:
                self.state_trans()

        # state 7
        elif self.current_state == statesets["state_7_user3"]:

            if self.my_color.color_send(img, 'brown'):  # 识别棕色，用户3
                if self.my_ball.color_type == color_type["brown"]:
                    self.my_ball.send_ball()  # 匹配开舱门并reset
                self.state_trans()

    def state_trans(self):
        """ 状态转移函数 """
        global flag_grass
        info = reveive_data()  # stm32 返回数据
        # state 1
        if self.current_state == statesets["state_1_start"]:
            if info == '1':
                self.current_state = statesets["state_2_load"]  # 状态切换

                change_symbol('state_2_load')
                light.pulse_width_percent(1)  # 补充亮度用于识别小球

        # state 2
        elif self.current_state == statesets["state_2_load"]:
            if info == '2':
                self.current_state = statesets["state_3_user1"]  # 状态切换

                change_symbol('state_3_user1')
                light.pulse_width_percent(0)  # 识别小球完毕，关闭补光板

        # state 3
        elif self.current_state == statesets["state_3_user1"]:

            if info == '3':
                self.current_state = statesets["state_4_stair"]  # 状态切换
                change_symbol('state_4_stair', 4)

        # state 4
        elif self.current_state == statesets["state_4_stair"]:
            if info == '4':
                self.current_state = statesets["state_5_user2"]  # 状态切换
                change_symbol('state_5_user2', 4)

        # state 5
        elif (self.current_state == statesets["state_5_user2"]):
            if info == '5':
                self.current_state = statesets["state_6_grass"]  # 状态切换
                change_symbol('state_6_grass', 1)
                light.pulse_width_percent(100)  # 打开补光版，草地用

        # state 6
        elif self.current_state == statesets["state_6_grass"]:
            if info == '6':
                self.current_state = statesets["state_7_user3"]  # 状态切换
                light.pulse_width_percent(0)  # 关闭补光版
                flag_grass = 0
                change_symbol('state_7_user3', 1)

        # state 7
        elif self.current_state == statesets["state_7_user3"]:
            if info == '7':
                self.current_state = statesets["state_1_start"]  # 状态切换
                change_symbol('state_1_start', 1)


def change_symbol(state, sleep_time=1):
    """状态转移成功后oopenmv绿灯亮

    Args:
        sleep_time (int, optional): 持续时间 /s. Defaults to 1.
    """
    str = "change to " + state
    print(str)
    LED(2).on()
    time.sleep(sleep_time)
    LED(2).off()
