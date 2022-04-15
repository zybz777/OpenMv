"""
    状态机
"""
from color_detect import detect_black_obstacle, detect_blue_start_point, detect_user, detect_yellow_upstair, detect_grass, detect_bucket_obstacle
from ball_detect import detect_ball
from line_detect import my_line
from uart import my_uart
from utils import COLOR, STATE
import sensor
import pyb
from pyb import Pin, Timer, LED
yellow_time = 0

light = Timer(2, freq=50000).channel(1, Timer.PWM, pin=Pin("P6"))
# TODO：依托于颜色判断很准才可以
class State_Machine():
    def __init__(self):
        self.state = STATE['state_1_begin']
        self.ball_time = 0
        self.now_time = 0
        self.yellow_time = 0
        self.bucket_time = 0

    def state_machine_exe(self, img):
        if self.state == STATE['state_1_begin']:
            if self.find_starting_point(img) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_recognize_ball'])
                light.pulse_width_percent(3) # 控制亮度 0~100
            else:
                my_line.line_track(img.copy(),err=1,type='turn', angle_limit=30)
                my_uart.send_data()
            my_uart.clear_data()
            """ 识别球 """
        elif self.state == STATE['state_recognize_ball']:
            if self.find_ball(img) is True:  # 识别球
                my_uart.send_data()
                self.state_trans(STATE['state_2_user1'])
            else:
                my_line.line_track(img.copy())
                my_uart.send_data()
            my_uart.clear_data()
            """ 到达用户1区域 """
        elif self.state == STATE['state_2_user1']:
            if self.find_user(img, 1) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_3_yellow_climb'])
            else:
                my_line.line_track(img.copy(),err=5)
                my_uart.send_data()
            my_uart.clear_data()
            """ 准备上台阶  """
        elif self.state == STATE['state_3_yellow_climb']:
            if self.find_yellow_upstair(img) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_4_black_obstacle'])
                #self.yellow_time = pyb.millis()  # 从启动开始的毫秒数
            else:
                my_line.line_track(img.copy(),err=1,type='turn', angle_limit=30)
                my_uart.send_data()
            my_uart.clear_data()
            """ 准备绕柱子  """
        elif self.state == STATE['state_4_black_obstacle']:
            #TODO: 该状态经测试发现不需要存在，直接跳转到下一状态
            #self.state = STATE['state_5_user2']
            self.state_trans(STATE['state_5_user2'])
            self.yellow_time = pyb.millis()  # 从启动开始的毫秒数
            light.pulse_width_percent(3) # 控制亮度 0~100完成
            """ 到达用户2区域 """
        elif self.state == STATE['state_5_user2']:
            if self.find_user(img, 2) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_6_grass'])
                light.pulse_width_percent(3) # 控制亮度 0~100完成
            else:
                self.now_time = pyb.millis()
                if self.now_time - self.yellow_time < 34500:
                    my_line.line_track(img.copy())
                else:
                    print("切换至笨比步态")
                    light.pulse_width_percent(0)
                    my_uart.set_data(1, 'isOpen')
                    my_line.line_track(img.copy(),err=14)
                my_uart.send_data()
            my_uart.clear_data()
            """ 到达草地 """
        elif self.state == STATE['state_6_grass']:
            if self.find_grass(img) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_7_user3'])
            else:
                my_line.line_track(img.copy(),err=1,type='turn', angle_limit=30)
                my_uart.send_data()
            my_uart.clear_data()
            """ 到达用户3区域 """
        elif self.state == STATE['state_7_user3']:
            if self.find_user(img, 3) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_1_begin'])
                light.pulse_width_percent(10) # 控制亮度 0~100
            else:
                if detect_grass(img) is True:
                    my_line.line_track_grass(img.copy())
                else:
                    my_line.line_track(img.copy(),type='grass')
                my_uart.send_data()
            my_uart.clear_data()
        else:
            pass

    def state_trans(self, st):
        N = 20
        if st == STATE['state_recognize_ball']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '1' in info:
                    self.state = st  # 状态转移成功
                    print("准备接收球")
                    break
        elif st == STATE['state_2_user1']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '2' in info:
                #if info != '0':
                    self.state = st  # 状态转移成功
                    print('准备检测用户1')
                    break
        elif st == STATE['state_3_yellow_climb']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '3' in info:
                #if info != '0':
                    self.state = st  # 状态转移成功
                    print('准备上台阶')
                    break
        elif st == STATE['state_4_black_obstacle']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '4' in info:
                #if info != '0':
                    self.state = st  # 状态转移成功
                    print('准备绕过柱子')
                    break
        elif st == STATE['state_5_user2']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '5' in info:
                #if info != '0':
                    self.state = st  # 状态转移成功
                    print('准备检测用户2')
                    break
        elif st == STATE['state_6_grass']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '6' in info:
                #if info != '0':
                    self.state = st
                    print('准备检测草地')
                    break
        elif st == STATE['state_7_user3']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '7' in info:
                #if info != '0':
                    self.state = st
                    print('准备检测用户3')
                    break
        elif st == STATE['state_1_begin']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '8' in info:
                #if info != '0':
                    self.state = st
                    print('准备检测起点')
                    break
        else:
            pass

    def find_starting_point(self, img):
        """识别起点 黑+蓝

        Args:
            img (img): img

        Returns:
            Bool: True or False
        """
        # 黑色障碍
        FLAG_BALCK = detect_black_obstacle(img)
        if FLAG_BALCK is not True:
            return False
        FLAG_BLUE = detect_blue_start_point(img)
        # 蓝色起点提示
        if FLAG_BLUE is not True:
            return False
        # 识别成功
        print('到达起点')
        my_uart.set_data(COLOR['BLUE'], 'color')  # set message by uart
        return True

    def find_ball(self, img):
        """识别三颜色的球

        Args:
            img (_type_): _description_

        Returns:
            Bool: True of False
        """
        self.FLAG_BALL_TYPE = {'RED': False, 'PRUPLE': False, 'BROWN': False}
        self.FLAG_BALL_TYPE['RED'] = detect_ball(img, 'RED')
        self.FLAG_BALL_TYPE['PRUPLE'] = detect_ball(img, 'PRUPLE')
        self.FLAG_BALL_TYPE['BROWN'] = detect_ball(img, 'BROWN')
        # 识别成功
        if self.FLAG_BALL_TYPE['RED'] is True or self.FLAG_BALL_TYPE['PRUPLE'] is True or self.FLAG_BALL_TYPE['BROWN'] is True:
            my_uart.set_data(1, 'ball')  # 检测到球
            if self.FLAG_BALL_TYPE['PRUPLE'] is True:
                my_uart.set_data(COLOR['PRUPLE'], 'color')
                print("找到紫球")
            elif self.FLAG_BALL_TYPE['BROWN'] is True:
                my_uart.set_data(COLOR['BROWN'], 'color')
                print("找到棕球")
            elif self.FLAG_BALL_TYPE['RED'] is True:
                my_uart.set_data(COLOR['RED'], 'color')
                print("找到红球")
            return True
        # 识别失败
        else:
            my_uart.set_data(0, 'ball')
            my_uart.set_data(COLOR['BLACK'], 'color')
            return False

    def find_user(self, img, id: int):
        """find_user 识别用户颜色 红、棕、紫

        Args:
            img (_type_): _description_
            id (int): 用户序号

        Returns:
            Bool: True of False
        """
        id_list = {'1': 'RED', '2': 'BROWN', '3': 'PRUPLE'}
        FLAG_USER = detect_user(img, id)
        if FLAG_USER is not True:
            return False
        my_uart.set_data(COLOR[id_list[str(id)]], 'color')  # 开舱门 user1
        print('到达用户' + str(id) + '区域')
        return True

    def find_yellow_upstair(self, img):
        """find_yellow_upstair 识别楼梯 黑+黄

        Args:
            img (_type_): _description_

        Returns:
            Bool: True or False
        """
        # 黑色提示
        FLAG_BALCK = detect_black_obstacle(img)
        if FLAG_BALCK is not True:
            return False
        # 黄色台阶信息
        FLAG_YELLOW = detect_yellow_upstair(img)
        if FLAG_YELLOW is not True:
            return False
        # 识别成功
        print("到达台阶")
        my_uart.set_data(COLOR['YELLOW'], 'color')
        return True

    def find_grass(self, img):
        """find_grass 识别草地

        Args:
            img (_type_): _description_

        Returns:
            Bool: True or False
        """
        # TODO： 切换步态？ 需要开补光灯
        FLAG_GRASS = detect_grass(img)
        if FLAG_GRASS is not True:
            return False
        my_uart.set_data(COLOR['GREEN'], 'color')
        print('到达草地')
        return True

    def find_bucket_obstacles(self, img):
        """find_bucket_obstacles 识别桶状障碍物

        Args:
            img (_type_): _description_

        Returns:
            Bool: True of False
        """
        # TODO: 需要根据白线转向
        FLAG_BALCK = detect_bucket_obstacle(img, ROI=(0, 20, 80, 20))  # 上半屏幕
        if FLAG_BALCK is not True:
            return False
        print('到达桶装障碍物')
        my_uart.set_data(COLOR['BUCKET'], 'color')
        return True


state_machine = State_Machine()
