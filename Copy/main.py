# 主函数 - By: zyb - 周一 10月 25 2021
import sensor, image, time
import colorDef as CD
import lineDef as LD
import data as DA
"""    初始化openmv     """
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
"""    变量定义   """
state = 1
count = 0 # 用来控制颜色识别及发送数据的次数
N = 10 # count 比较数值

"""    主循环    """
while True:
    clock.tick()
    img = sensor.snapshot()
    """ ------颜色检测------- """
    if state == 1: # 识别蓝色，准备装载小球
        if CD.colorSend(img, 'blue') == CD.blue:
            count = count + 1
            print('blue')
        if count > N: # 发送10次数据，需要测试stm32的接受效果
            count = 0
            state = 2

    elif state == 2: # 小球判断
        CD.ballRecog(img)
        if CD.ballColor != 0: # 识别到小球
            state = 3

    elif state == 3: # 识别绿色，用户1，是否开舱门
        if CD.colorSend(img, 'green') == CD.green:
            CD.ballColorMatch(img)  # 匹配开舱门
            count = count + 1
        if count > N:
            count = 0
            state = 4

    elif state == 4: # 识别黄色，上台阶
        if CD.colorSend(img, 'yellow') == CD.yellow:
            count = count + 1
        if count > N:
            count = 0
            state = 5

    elif state == 5: # 识别红色，用户2，是否开舱门，且下斜坡
        if CD.colorSend(img, 'red') == CD.red:
            CD.ballColorMatch(img)  # 匹配开舱门
            count = count + 1
        if count > N:
            count = 0
            state = 6

    elif state == 6: # 识别绿色，草地，可能需要多声明一个串口信息位
        if CD.colorSend(img, 'green') == CD.green:
            count = count + 1
        if count > N:
            count = 0
            state = 7

    elif state == 7: # 识别棕色，用户3，是否开舱门
        if CD.colorSend(img, 'brown') == CD.brown:
            CD.ballColorMatch(img)  # 匹配开舱门
            count = count + 1
        if count > N:
            count = 0
            state = 1

    """ ------赛道检测------ """
    LD.line_track(img.copy())
    # print(LD.line_track(img))
    """ ------数据发送------ """
    DA.sendData()
    DA.clearData()
    print(clock.fps()) # 显示FPS
