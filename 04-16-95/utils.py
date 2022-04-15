COLOR_THRESHOLD = {
    'BLACK': [(1, 80, -5, 9, -6, 11)],  # version 1
    'BLUE': [(12, 40, -5, 14, -36, -14)],  # version 3
    'RED': [(21, 39, 11, 59, 3, 37)],  # version 2
    'YELLOW': [(57, 99, -26, -2, 10, 52)],  # version 3
    'BROWN': [(11, 43, 11, 41, 4, 33)],  # version 2
    'GREEN': [(0, 45, -38, -19, 0, 56)],  # version 2
    'PRUPLE': [(0, 45, 12, 127, -128, 127)]  # version 1

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
    'RED': [(29, 57, 34, 127, -128, 127)],  # version2
    'BROWN': [(30, 65, 10, 38, 22, 127)], # version3
    'PRUPLE': [(0, 38, 6, 31, -52, -18)], # verion2
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
