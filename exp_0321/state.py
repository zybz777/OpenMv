"""
    状态函数
"""
from color_detect import detect_black_obstacle, detect_blue_start_point, detect_user
from ball_detect import detect_ball
from uart import my_uart
from utils import COLOR


# TODO: 加狗子串口反馈， 每一个函数内部，没收到狗子对应信息就一直执行 ？
class State_Machine():
    def __init__(self):
        self.FLAG_BALL_TYPE = {'RED': False, 'BROWN': False, 'PRUPLE': False}
        self.FLAG_START = False  # TODO：识别到起点后变为True, 走到用户区成功送球复位
        pass

    def run(self, img):
        if self.FLAG_START is False:
            self.FLAG_START = self.find_starting_point(img)  # 找到起点， 发送消息
        if self.FLAG_START is True and (self.FLAG_BALL_TYPE['RED'] is False and self.FLAG_BALL_TYPE['BROWN'] is False
                                        and self.FLAG_BALL_TYPE['PRUPLE'] is False):
            self.find_ball(img)  # 识别球
        flag_user = self.find_user(img)
        if flag_user is True:
            self.FLAG_START = False  # 球已送达，复位起点状态为

    def find_starting_point(self, img):
        """find starting point and set uart data

        Args:
            img (img): img

        Returns:
            Bool: True or False
        """
        FLAG_BALCK = detect_black_obstacle(img)
        if FLAG_BALCK is not True:
            return False
        FLAG_BLUE = detect_blue_start_point(img)
        if FLAG_BLUE is not True:
            return False
        print('到达起点')
        # TODO: 串口发送消息， 接收 STM 消息
        my_uart.set_data(COLOR['BLUE'], 'color')  # set message by uart
        return True

    def find_ball(self, img):
        self.FLAG_BALL_TYPE['RED'] = detect_ball(img, 'RED')
        self.FLAG_BALL_TYPE['PRUPLE'] = detect_ball(img, 'PRUPLE')
        self.FLAG_BALL_TYPE['BROWN'] = detect_ball(img, 'BROWN')
        if self.FLAG_BALL_TYPE['RED'] is True or self.FLAG_BALL_TYPE['PRUPLE'] is True or self.FLAG_BALL_TYPE['BROWN'] is True:
            my_uart.set_data(1, 'ball')  # 检测到球
        else:
            my_uart.set_data(0, 'ball')
        return self.FLAG_BALL_TYPE

    def find_user(self, img):
        # 根据球的颜色信息寻找对应, 状态为为临时变量 不需要复位
        if self.FLAG_BALL_TYPE['RED'] is True:
            FLAG_USER1 = detect_user(img, 1)
            if FLAG_USER1 is True:
                my_uart.set_data(1, 'isOpen')  # 开舱门 user1
                return True
        elif self.FLAG_BALL_TYPE['BROWN'] is True:
            FLAG_USER2 = detect_user(img, 2)
            if FLAG_USER2 is True:
                my_uart.set_data(1, 'isOpen')  # 开舱门 user2
                return True
        elif self.FLAG_BALL_TYPE['PRUPLE'] is True:
            FLAG_USER3 = detect_user(img, 3)
            if FLAG_USER3 is True:
                my_uart.set_data(1, 'isOpen')  # 开舱门 user3
                return True
        return False


state_machine = State_Machine()
