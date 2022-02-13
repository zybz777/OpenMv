color_type = {
    'black': 0,
    'green': 1,
    'red': 2,
    'browm': 3,
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

def find_max_blob(blobs):
    """ 寻找最大颜色块 """
    maxSize = 0
    for blob in blobs:
        nowSize = blob.w() * blob.h()
        if nowSize > maxSize:
            maxBlob = blob
            maxSize = nowSize
    return maxBlob