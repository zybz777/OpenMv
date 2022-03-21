from utils import COLOR_THRESHOLD, COLOR
from color_detect import get_max_blob


def detect_ball(img, input_color):
    ROI = (0, 20, 80, 40)  # 下 2/3 屏幕
    blobs = img.find_blobs(COLOR_THRESHOLD[input_color], merge=True, margin=10, roi=ROI, x_stride=5, y_stride=5)
    if blobs is None:
        return False

    blob = get_max_blob(blobs)
    # exit 2
    if blob is None:
        return False
    x, y, w, h = blob.cx(), blob.cy(), blob.w(), blob.h()
    ratio = round(w / h, 2)
    ratio_limit = [0.8, 1.2]

    if ratio_limit[0] < ratio and ratio < ratio_limit[1]:
        img.draw_rectangle(blob.rect())
        return True