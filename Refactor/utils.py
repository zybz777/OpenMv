"""重构 公共变量存储 - By: zyb - 周日 2月 13 2022
"""
color_type = {
    'black': 0,
    'green': 1,
    'red': 2,
    'brown': 3,
    'yellow': 4,
    'blue': 5
}

color_threshold = {
    'black': {
        'threshold': [(1, 2, -2, -1, 0, 0)]
    },
    'brown': {
        'threshold': [(43, 60, -13, 16, 21, 62)]
    },
    'red': {
        'threshold': [(22, 60, 7, 42, -46, 11)]
    },
    'green': {
        'threshold': [(40, 76, -40, -17, 20, 40)]  # 阈值偏暗，在光线充足下识别不出
    },
    'yellow': {
        'threshold': [(54, 72, -26, -4, 17, 59)]
    },
    'blue': {
        'threshold': [(45, 68, -28, 21, -32, -8)]
    }
}

statesets = {
    "state_1_start": 1,
    "state_2_load": 2,
    "state_3_user1": 3,
    "state_4_stair": 4,
    "state_5_user2": 5,
    "state_6_grass": 6,
    "state_7_user3": 7
}
RedLab = color_threshold['red']['threshold'][0]
GreenLab = color_threshold['green']['threshold'][0]
BrownLab = color_threshold['brown']['threshold'][0]


def find_max_blob(blobs):
    """ 寻找最大颜色块 """
    maxSize = 0
    maxBlob = None
    for blob in blobs:
        nowSize = blob.w() * blob.h()
        if nowSize > maxSize:
            maxBlob = blob
            maxSize = nowSize
    return maxBlob
