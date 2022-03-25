"""
    状态函数
"""
from color_detect import detect_black_obstacle, detect_blue_start_point, detect_user, detect_yellow_upstair, detect_grass
from ball_detect import detect_ball
from uart import my_uart
from utils import COLOR
import sensor

STATE = {
    'state_1_begin': 1,
    'state_recognize_ball': 2,
    'state_2_user1': 3,
    'state_3_yellow_climb': 4,
    'state_4_black_obstacle': 5,
    'state_5_user2': 6,
    'state_6_grass': 7,
    'state_7_user3': 8,
    'state_debug': 9
}


# TODO：依托于颜色判断很准才可以
class State_Machine():
    def __init__(self):
        self.FLAG_BALL_TYPE = {'RED': False, 'BROWN': False, 'PRUPLE': False}  # 三球状态位
        self.FLAG_START = False  # TODO：识别到起点后变为True, 走到用户区成功送球复位
        self.state = STATE['state_1_begin']

    def state_machine_exe(self, img):
        if self.state == STATE['state_1_begin']:
            # flag1 = self.find_starting_point(img)
            if self.find_starting_point(img) is True:
                my_uart.send_data()  # 发送蓝色
                my_uart.clear_data()
                self.state_trans(STATE['state_recognize_ball'])
            else:
                pass
            """ 识别球 """
        elif self.state == STATE['state_recognize_ball']:
            if self.find_ball(img) is True:  # 识别球
                my_uart.send_data()  # 发送球和球颜色
                my_uart.clear_data()
                self.state_trans(STATE['state_2_user1'])
            else:
                pass
            """ 到达用户1区域 """
        elif self.state == STATE['state_2_user1']:
            if self.find_user(img, 1) is True:
                my_uart.send_data()  # 发送球和球颜色
                my_uart.clear_data()
                self.state_trans(STATE['state_3_yellow_climb'])
            else:
                pass
            """ 准备上台阶  """
        elif self.state == STATE['state_3_yellow_climb']:
            if self.find_yellow_upstair(img) is True:
                my_uart.send_data()  # 发送球和球颜色
                my_uart.clear_data()
                self.state_trans(STATE['state_4_black_obstacle'])
            else:
                pass
            """ 准备绕柱子  """
        elif self.state == STATE['state_4_black_obstacle']:
            if self.find_bucket_obstacles(img) is True:
                my_uart.send_data()  # 发送球和球颜色
                my_uart.clear_data()
                self.state_trans(STATE['state_5_user2'])
            else:
                pass
            """ 到达用户2区域 """
        elif self.state == STATE['state_5_user2']:
            if self.find_user(img, 2) is True:
                my_uart.send_data()  # 发送球和球颜色
                my_uart.clear_data()
                self.state_trans(STATE['state_6_grass'])
            else:
                pass
            """ 到达草地 """
        elif self.state == STATE['state_6_grass']:
            if self.find_grass(img) is True:
                my_uart.send_data()
                my_uart.clear_data()
                self.state_trans(STATE['state_7_user3'])
            else:
                pass
            """ 到达用户3区域 """
        elif self.state == STATE['state_7_user3']:
            if self.find_user(img, 3) is True:
                my_uart.send_data()  # 发送球和球颜色
                my_uart.clear_data()
                self.state_trans(STATE['state_1_begin'])
            else:
                pass
        else:
            pass

    def state_trans(self, st):
        info = my_uart.reveive_data()
        if st == STATE['state_recognize_ball']:
            if '1' in info:
                self.state = st  # 状态转移成功
                print("准备接收球")
        elif st == STATE['state_2_user1']:
            if '2' in info:
                self.state = st  # 状态转移成功
                print('准备检测用户1')
        elif st == STATE['state_3_yellow_climb']:
            if '3' in info:
                self.state = st  # 状态转移成功
                print('准备上台阶')
        elif st == STATE['state_4_black_obstacle']:
            if '4' in info:
                self.state = st  # 状态转移成功
                print('准备绕过柱子')
        elif st == STATE['state_5_user2']:
            if '5' in info:
                self.state = st  # 状态转移成功
                print('准备检测用户2')
        elif st == STATE['state_6_grass']:
            if '6' in info:
                self.state = st
                print('准备检测草地')
        elif st == STATE['state_7_user3']:
            if '7' in info:
                self.state = st
                print('准备检测用户3')
        elif st == STATE['state_1_begin']:
            if '8' in info:
                self.state = st
                print('准备检测起点')
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
        # TODO: 串口发送消息， 接收 STM 消息
        my_uart.set_data(COLOR['BLUE'], 'color')  # set message by uart
        return True

    def find_ball(self, img):
        """识别三颜色的球

        Args:
            img (_type_): _description_

        Returns:
            Bool: True of False
        """
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
        if detect_user(img, id) is True:
            # my_uart.set_data(1, 'isOpen')  # 开舱门 user1
            my_uart.set_data(COLOR[id_list[str(id)]], 'color')  # 开舱门 user1
            print('到达用户' + str(id) + '区域')
            return True
        else:
            return False

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
        if FLAG_GRASS is True:
            my_uart.set_data(COLOR['GREEN'], 'color')
            print('到达草地')
            return True
        return False

    def find_bucket_obstacles(self, img):
        """find_bucket_obstacles 识别桶状障碍物

        Args:
            img (_type_): _description_

        Returns:
            Bool: True of False
        """
        # TODO: 需要根据白线转向
        FLAG_BALCK = detect_black_obstacle(img, ROI=(0, 0, 80, 20))  # 上半屏幕
        if FLAG_BALCK is not True:
            return False
        print('到达桶装障碍物')
        my_uart.set_data(COLOR['BUCKET'], 'color')
        return True


state_machine = State_Machine()
