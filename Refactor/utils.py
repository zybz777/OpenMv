COLOR_THRESHOLD = {
    'BLACK': [(0, 13, -16, 3, 0, 14)],  # version 1
    'BLUE': [(12, 40, -5, 14, -36, -14)],  # version 3
    'RED': [(21, 39, 11, 59, 3, 37)],  # version 2
    'YELLOW': [(60, 87, -26, -2, 15, 56)],  # version 2
    'BROWN': [(11, 43, 11, 32, 4, 33)],  # version 2
    'GREEN': [(47, 88, -47, -10, 12, 59)],  # version 2
    'PRUPLE': [(11, 25, 4, 30, -20, 0)]  # version 1
}

COLOR = {
    'BLACK': 0,
    'BLUE': 1,
    'RED': 2,
    'YELLOW': 3,
    'BROWN': 4,
    'GREEN': 5,
    'PRUPLE': 6,
    'BUCKET': 7,
}

BALL_COLOR_THRESHOLD = {
    'RED': [(16, 32, 13, 50, 21, 35)],  # version2
    'BROWN': [(35, 60, 7, 40, 40, 56)], # version3
    'PRUPLE': [(1, 32, 1, 28, -42, -7)], # verion2
}

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
