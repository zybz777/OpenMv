"""
    状态函数
"""
from color_detect import detect_black_obstacle, detect_blue_start_point
from uart import my_uart
from utils import COLOR


def find_starting_point(img):
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
