"""
    状态函数
"""
from color_detect import detect_black_obstacle, detect_blue_start_point, detect_user, detect_yellow_upstair, detect_grass
from ball_detect import detect_ball
from uart import my_uart
from utils import COLOR
import sensor


# TODO：依托于颜色判断很准才可以
class State_Machine():
    def __init__(self):
        self.FLAG_BALL_TYPE = {'RED': False, 'BROWN': False, 'PRUPLE': False}  # 三球状态位
        self.FLAG_START = False  # TODO：识别到起点后变为True, 走到用户区成功送球复位

    def run(self, img):
        # 找起点
        if self.FLAG_START is False:
            while True:
                img = sensor.snapshot()
                self.FLAG_START = self.find_starting_point(img)  # 找到起点， 发送消息
                my_uart.send_data()  # 发送该颜色信息
                info = my_uart.reveive_data()
                my_uart.clear_data()
                # 接收狗子信息， 退出该状态
                if '1' in info:
                    self.FLAG_START = True
                    print("准备接收球")
                    break

        # 找球, 依托于起点识别
        if self.FLAG_START is True and (self.FLAG_BALL_TYPE['RED'] is False and self.FLAG_BALL_TYPE['BROWN'] is False
                                        and self.FLAG_BALL_TYPE['PRUPLE'] is False):
            while True:
                img = sensor.snapshot()
                self.find_ball(img)  # 识别球
                my_uart.send_data()  # 发送该颜色信息
                info = my_uart.reveive_data()
                my_uart.clear_data()
                # 接收狗子信息， 退出该状态
                if '2' in info:
                    if self.FLAG_BALL_TYPE['RED'] is True:
                        print("红球接收完毕")
                    if self.FLAG_BALL_TYPE['BROWN'] is True:
                        print("棕球接收完毕")
                    if self.FLAG_BALL_TYPE['PRUPLE'] is True:
                        print("紫球接收完毕")
                    break

        # 找用户, 依托于球判断准确，只会在球对应颜色用户区停车
        flag_user = self.find_user(img)
        if flag_user is True:
            while True:
                img = sensor.snapshot()
                self.find_user(img)
                my_uart.send_data()  # 发送该颜色信息
                info = my_uart.reveive_data()
                my_uart.clear_data()
                # 接收狗子信息， 退出该状态
                if '3' in info:
                    print("快递球投递成功")
                    self.FLAG_START = False  # 球已送达，复位起点状态
                    self.FLAG_BALL_TYPE['RED'] = False
                    self.FLAG_BALL_TYPE['BROWN'] = False
                    self.FLAG_BALL_TYPE['PRUPLE'] = False

        # 找障碍
        flag_upstair = self.find_yellow_upstair(img)  # 障碍1
        if flag_upstair is True:
            while True:
                img = sensor.snapshot()
                self.find_yellow_upstair(img)
                my_uart.send_data()  # 发送该颜色信息
                info = my_uart.reveive_data()
                my_uart.clear_data()
                if '4' in info:
                    print("到达上台阶")
                    break

        self.find_bucket_obstacles(img)  # 障碍2
        self.find_grass(img)  # 障碍3

    def find_starting_point(self, img):
        """find starting point and set uart data

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
        """find_ball 找三个球，将颜色信息存储到 FLAG_BALL_TYPE 中， 串口发送是否有球

        Args:
            img (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.FLAG_BALL_TYPE['RED'] = detect_ball(img, 'RED')
        self.FLAG_BALL_TYPE['PRUPLE'] = detect_ball(img, 'PRUPLE')
        self.FLAG_BALL_TYPE['BROWN'] = detect_ball(img, 'BROWN')
        # 识别成功
        if self.FLAG_BALL_TYPE['RED'] is True or self.FLAG_BALL_TYPE['PRUPLE'] is True or self.FLAG_BALL_TYPE['BROWN'] is True:
            my_uart.set_data(1, 'ball')  # 检测到球
            print("找到球")
        # 识别失败
        else:
            my_uart.set_data(0, 'ball')
        return self.FLAG_BALL_TYPE

    def find_user(self, img):
        """find_user  判断三位用户哪位需要投递球， 串口发送消息

        Args:
            img (_type_): _description_

        Returns:
            _type_: _description_
        """
        # 根据球的颜色信息寻找对应, 状态为为临时变量 不需要复位
        if self.FLAG_BALL_TYPE['RED'] is True:
            FLAG_USER1 = detect_user(img, 1)
            if FLAG_USER1 is True:
                my_uart.set_data(1, 'isOpen')  # 开舱门 user1
                print('找到红色用户')
                return True
        elif self.FLAG_BALL_TYPE['BROWN'] is True:
            FLAG_USER2 = detect_user(img, 2)
            if FLAG_USER2 is True:
                my_uart.set_data(1, 'isOpen')  # 开舱门 user2
                print('找到棕色用户')
                return True
        elif self.FLAG_BALL_TYPE['PRUPLE'] is True:
            FLAG_USER3 = detect_user(img, 3)
            if FLAG_USER3 is True:
                my_uart.set_data(1, 'isOpen')  # 开舱门 user3
                print('找到紫色用户')
                return True
        # 识别失败
        return False

    def find_yellow_upstair(self, img):
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
        # TODO： 切换步态？ 需要开补光灯
        FLAG_GRASS = detect_grass(img)
        if FLAG_GRASS is True:
            my_uart.set_data(COLOR['GREEN'], 'color')
            print('到达草地')

    def find_bucket_obstacles(self, img):
        # TODO: 需要根据白线转向
        pass


state_machine = State_Machine()
