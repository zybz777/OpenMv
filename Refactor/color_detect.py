from utils import COLOR_THRESHOLD, COLOR
"""
    img
        w: 80
        h: 60
"""


def detect_black_obstacle(img, ROI=(0, 50, 80, 10)):
    """detect_color, ROI为下半屏幕, 最低限制为ROI的1/4

    Args:
        img (img): img
        input_color (str): BLACK, BLUE etc.
    """
    Area_th = int((ROI[2] * ROI[3]) / 4)  # ROI 区域的 1/4
    blobs = img.find_blobs(COLOR_THRESHOLD['BLACK'], merge=True, area_threshold=Area_th, margin=20, roi=ROI, x_stride=40, y_stride=6)
    # exit 1
    if blobs is None:
        return False

    # display color rect
    blob = get_max_blob(blobs)
    # exit 2
    if blob is None:
        return False

    x, y, w, h = blob.cx(), blob.cy(), blob.w(), blob.h()
    # print(x, y, w, h) # display [x y w h]
    # print('Area', w * h)  # display area
    ratio = round(w / h, 2)
    ratio_limit = 2  # TODO: 需要赛道实测，先给出一个大概值
    # exit 3
    if ratio < ratio_limit:
        return False

    # print("ratio", round(w / h, 2))  # display ratio
    img.draw_rectangle(blob.rect())
    img.draw_string(x, y, 'black', color=(255, 255, 255))
    return True


def detect_blue_start_point(img, ROI=(0, 30, 80, 30)):
    """detect_blue_start_point ROI为中间1/3屏幕, 最低限制为ROI的1/4

    Args:
        img (_type_): _description_

    Returns:
        _type_: _description_
    """
    Area_th = int((ROI[2] * ROI[3]) / 100)  # ROI 区域的 1/4
    blobs = img.find_blobs(COLOR_THRESHOLD['BLUE'], merge=True, area_threshold=Area_th, margin=10, roi=ROI, x_stride=40, y_stride=6)
    # exit 1
    if blobs is None:
        return False

    blob = get_max_blob(blobs)
    # exit 2
    if blob is None:
        return False

    x, y, w, h = blob.cx(), blob.cy(), blob.w(), blob.h()
    # print(x, y, w, h) # display [x y w h]
    # print('Area', w * h)  # display area
    ratio = round(w / h, 2)
    ratio_limit = 2  # TODO: 需要赛道实测，先给出一个大概值
    # exit 3
    if ratio < ratio_limit:
        return False

    # print("ratio", round(w / h, 2))  # display ratio
    img.draw_rectangle(blob.rect())
    img.draw_string(x, y, 'blue', color=(255, 255, 255))
    return True


def detect_user(img, id: int, ROI=(0, 40, 80, 20)):
    """detect_user ROI为最下1/3屏幕, 最低限制为ROI的1/4

    Args:
        img (_type_): _description_
        id (int): _description_

    Returns:
        _type_: _description_
    """
    ID_dict = {'1': 'RED', '2': 'BROWN', '3': 'PRUPLE'}

    Area_th = int((ROI[2] * ROI[3]) / 4)  # ROI 区域的 1/4
    blobs = img.find_blobs(COLOR_THRESHOLD[ID_dict[str(id)]], merge=True, area_threshold=Area_th, margin=10, roi=ROI, x_stride=40, y_stride=6)
    # exit 1
    if blobs is None:
        return False

    blob = get_max_blob(blobs)
    # exit 2
    if blob is None:
        return False

    x, y, w, h = blob.cx(), blob.cy(), blob.w(), blob.h()
    # print(x, y, w, h) # display [x y w h]
    # print('Area', w * h)  # display area
    ratio = round(w / h, 2)
    ratio_limit = 2  # TODO: 需要赛道实测，先给出一个大概值
    # exit 3
    if ratio < ratio_limit:
        return False

    # print("ratio", round(w / h, 2))  # display ratio
    img.draw_rectangle(blob.rect())
    img.draw_string(x, y, ID_dict[str(id)], color=(255, 255, 255))
    return True


def detect_yellow_upstair(img, ROI=(0, 20, 80, 20)):
    """detect_yellow_upstair ROI为中间1/3屏幕, 最低限制为ROI的1/4

    Args:
        img (_type_): _description_

    Returns:
        _type_: _description_
    """
    Area_th = int((ROI[2] * ROI[3]) / 4)  # ROI 区域的 1/4
    blobs = img.find_blobs(COLOR_THRESHOLD['YELLOW'], merge=True, area_threshold=Area_th, margin=10, roi=ROI, x_stride=40, y_stride=6)
    # exit 1
    if blobs is None:
        return False

    blob = get_max_blob(blobs)
    # exit 2
    if blob is None:
        return False

    x, y, w, h = blob.cx(), blob.cy(), blob.w(), blob.h()
    # print(x, y, w, h) # display [x y w h]
    # print('Area', w * h)  # display area
    ratio = round(w / h, 2)
    ratio_limit = 2  # TODO: 需要赛道实测，先给出一个大概值
    # exit 3
    if ratio < ratio_limit:
        return False

    # print("ratio", round(w / h, 2))  # display ratio
    img.draw_rectangle(blob.rect())
    img.draw_string(x, y, 'yellow', color=(255, 255, 255))
    return True


def detect_grass(img, ROI=(0, 20, 80, 40)):
    """detect_grass ROI为下2/3屏幕, 最低限制为ROI的1/4

    Args:
        img (_type_): _description_

    Returns:
        _type_: _description_
    """
    Area_th = int((ROI[2] * ROI[3]) / 4)  # ROI 区域的 1/4
    blobs = img.find_blobs(COLOR_THRESHOLD['GREEN'], merge=True, area_threshold=Area_th, margin=10, roi=ROI, x_stride=40, y_stride=6)
    # exit 1
    if blobs is None:
        return False

    blob = get_max_blob(blobs)
    # exit 2
    if blob is None:
        return False

    x, y, w, h = blob.cx(), blob.cy(), blob.w(), blob.h()
    # print(x, y, w, h) # display [x y w h]
    # print('Area', w * h)  # display area
    ratio = round(w / h, 2)
    ratio_limit = 0.8  # TODO: 需要赛道实测，先给出一个大概值 草地需要面积
    # exit 3
    if ratio < ratio_limit:
        return False

    # print("ratio", round(w / h, 2))  # display ratio
    img.draw_rectangle(blob.rect())
    img.draw_string(x, y, 'green', color=(255, 255, 255))
    return True


def detect_bucket_obstacle(img, ROI=(0, 0, 80, 20)):
    """detect_color, ROI为下半屏幕, 最低限制为ROI的1/4

    Args:
        img (img): img
        input_color (str): BLACK, BLUE etc.
    """
    Area_th = int((ROI[2] * ROI[3]) / 10)  # ROI 区域的 1/4
    blobs = img.find_blobs(COLOR_THRESHOLD['BLACK'], merge=True, area_threshold=Area_th, margin=20, roi=ROI, x_stride=40, y_stride=6)
    # exit 1
    if blobs is None:
        return False

    # display color rect
    blob = get_max_blob(blobs)
    # exit 2
    if blob is None:
        return False

    x, y, w, h = blob.cx(), blob.cy(), blob.w(), blob.h()
    # print(x, y, w, h) # display [x y w h]
    # print('Area', w * h)  # display area
    ratio = round(w / h, 2)
    ratio_limit = 0.5  # TODO: 需要赛道实测，先给出一个大概值
    # exit 3
    if ratio < ratio_limit:
        return False

    # print("ratio", round(w / h, 2))  # display ratio
    img.draw_rectangle(blob.rect())
    img.draw_string(x, y, 'black', color=(255, 255, 255))
    return True


def get_max_blob(blobs):
    """根据色块列表寻找最大色块

    Args:
        blobs (blobs): find_color 得到的色块集合

    Returns:
        blob: 最大色块
    """
    maxSize = 0
    maxBlob = None
    for blob in blobs:
        nowSize = blob.w() * blob.h()
        if nowSize > maxSize:
            maxBlob = blob
            maxSize = nowSize
    return maxBlob