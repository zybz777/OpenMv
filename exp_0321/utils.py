COLOR_THRESHOLD = {
    'BLACK': [(0, 13, -16, 3, 0, 14)],  # version 1
    'BLUE': [(12, 40, -5, 14, -36, -14)],  # version 3
    'RED': [(21, 39, 11, 59, 3, 37)],  # version 2
    'YELLOW': [(60, 87, -26, -2, 15, 56)],  # version 2
    'BROWN': [(42, 59, 11, 50, 8, 34)],  # version 1
    'GREEN': [(53, 81, -52, -36, 11, 44)],  # version 1
    'PRUPLE': [(45, 63, 20, 38, -57, -37)]  # version 1
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
    'RED': [(12, 35, 20, 46, 8, 38)],  # version2
    'BROWN': [(42, 59, 11, 50, 8, 34)],
    'PRUPLE': [(45, 63, 20, 38, -57, -37)],
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