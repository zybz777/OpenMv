"""重构 赛道状态机类 - By: zyb - 周日 2月 13 2022
"""
from detect_ball import Ball
from detect_color import Detect_color
from utils import statesets, color_type
from pyb import Pin, Timer, LED
import time

N = 3
count = 0
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
        self.my_ball = Ball()  # 声明球对象
        self.my_color = Detect_color()

    def state_exe(self, img):
        """ 状态执行函数 """
        global count, flag_grass
        # state 1
        if self.current_state == statesets["state_1_start"]:
            if self.my_color.color_send(img, 'blue'):  # 识别颜色
                count += 1  # 串口发送数据+1
            self.state_trans()
        # state 2
        elif self.current_state == statesets["state_2_load"]:
            self.my_ball.detect_ball(img)
            if self.my_ball.exists is True:  # 识别到小球
                count += 1  # 串口发送数据+1
            self.state_trans()
        # state 3
        elif self.current_state == statesets["state_3_user1"]:
            if self.my_color.color_send(img, 'green'):  # 识别颜色
                count += 1  # 串口发送数据+1
                if self.my_ball.color_type == color_type["green"]:
                    self.my_ball.send_ball()  # 匹配开舱门并reset
            self.state_trans()
        # state 4
        elif self.current_state == statesets["state_4_stair"]:
            if self.my_color.color_send(img, 'yellow'):  # 识别颜色
                count += 1  # 串口发送数据+1
            self.state_trans()
        # state 5
        elif self.current_state == statesets["state_5_user2"]:
            if self.my_color.color_send(img, 'red'):  # 识别颜色
                count += 1  # 串口发送数据+1
                if self.my_ball.color_type == color_type["red"]:
                    self.my_ball.send_ball()  # 匹配开舱门并reset
            self.state_trans()
        # state 6
        elif self.current_state == statesets["state_6_grass"]:
            if flag_grass == 0 and self.my_color.color_send(img,
                                                            'green') is True:
                flag_grass = 1
            elif flag_grass == 1 and self.my_color.color_send(img,
                                                              'green') is True:
                self.state_trans()
        # state 7
        elif self.current_state == statesets["state_7_user3"]:
            if self.my_color.color_send(img, 'brown'):  # 识别颜色
                count += 1  # 串口发送数据+1
                if self.my_ball.color_type == color_type["brown"]:
                    self.my_ball.send_ball()  # 匹配开舱门并reset
            self.state_trans()

    def state_trans(self, img):
        """ 状态转移函数 """
        global count, flag_grass
        # state 1
        if (count > N) and (self.current_state == statesets["state_1_start"]):
            self.current_state = statesets["state_2_load"]  # 状态切换
            print("now is state_2_load")
            count = 0
            LED(2).on()  # 状态切换标志
            time.sleep(sleep_time)
            LED(2).off()
            light.pulse_width_percent(1)
        # state 2
        elif (count > N) and (self.current_state == statesets["state_2_load"]):
            self.current_state = statesets["state_3_user1"]  # 状态切换
            print("now is state_3_user1")
            count = 0
            light.pulse_width_percent(0)
            LED(2).on()
            time.sleep(sleep_time)
            LED(2).off()
        # state 3
        elif (count > N) and (self.current_state
                              == statesets["state_3_user1"]):
            self.current_state = statesets["state_4_stair"]  # 状态切换
            print("now is state_4_stair")
            count = 0
            LED(2).on()
            time.sleep(4)
            LED(2).off()
        # state 4
        elif (count > N) and (self.current_state
                              == statesets["state_4_stair"]):
            self.current_state = statesets["state_5_user2"]  # 状态切换
            print("now is state_5_user2")
            count = 0
            LED(2).on()
            time.sleep(4)
            LED(2).off()
        # state 5
        elif (count > N) and (self.current_state
                              == statesets["state_5_user2"]):
            self.current_state = statesets["state_6_grass"]  # 状态切换
            print("now is state_6_grass")
            count = 0
            LED(2).on()
            time.sleep(1)
            LED(2).off()
            light.pulse_width_percent(100)  # 打开补光版，草地用
        # state 6
        elif (self.current_state == statesets["state_6_grass"]):
            self.current_state = statesets["state_7_user3"]  # 状态切换
            print("now is state_7_user3")
            count = 0
            light.pulse_width_percent(0)  # 关闭补光版
            flag_grass = 0
            LED(2).on()
            time.sleep(1)
            LED(2).off()
        # state 7
        elif (count > N) and (self.current_state
                              == statesets["state_7_user3"]):
            self.current_state = statesets["state_1_start"]  # 状态切换
            print("now is state_1_start")
            count = 0
            LED(2).on()
            time.sleep(1)
            LED(2).off()
