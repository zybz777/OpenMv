# 主函数 - By: zyb - 周一 10月 25 2021
import sensor, image, time
import colorDef as CD
import lineDef as LD
import data as DA
import pyb

from pyb import Pin, Timer, LED
import time
"""    初始化openmv     """
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
"""   补光版定义   """
light = Timer(2,
              freq=50000).channel(1, Timer.PWM,
                                  pin=Pin("P6"))  # 50kHz pin6 timer2 channel1
light.pulse_width_percent(0)  # 控制亮度 0~100
"""    变量定义   """
state = 1
count = 0  # 用来控制颜色识别及发送数据的次数
N = 50  # count 比较数值
"""    主循环    """
while True:
    clock.tick()
    img = sensor.snapshot()
    """ ------颜色检测------- """
    if state == 1:  # 识别蓝色，准备装载小球
        if CD.colorSend(img, 'blue') == CD.blue:
            count = count + 1

        if count > N:  # 发送10次数据，需要测试stm32的接受效果
            count = 0
            CD.ballColor = 0
            state = 2
            print('blue')
            print("state change")
            LED(2).on()
            time.sleep(1)
            light.pulse_width_percent(10)
            LED(2).off()

    elif state == 2:  # 小球判断
        CD.ballRecog(img)
        if CD.ballColor != 0:  # 识别到小球
            count += 1

        if count > N / 2:
            state = 3
            #if CD.ballColor == CD.green:
            #time.sleep(3)
            print("state change")
            LED(2).on()
            time.sleep(1)
            light.pulse_width_percent(0)
            LED(2).off()

    elif state == 3:  # 识别绿色，用户1，是否开舱门
        if CD.colorSend(img, 'green') == CD.green:
            CD.ballColorMatch(img)  # 匹配开舱门
            count = count + 1
        if count > N:
            count = 0
            state = 4
            print('green')
            LED(2).on()
            print("state change")
            time.sleep(1)
            LED(2).off()

    elif state == 4:  # 识别黄色，上台阶
        if CD.colorSend(img, 'yellow') == CD.yellow:
            count = count + 1
        if count > N:
            count = 0
            state = 5
            LED(2).on()
            print('yellow')
            print("state change")
            time.sleep(1)
            LED(2).off()

    elif state == 5:  # 识别红色，用户2，是否开舱门，且下斜坡
        if CD.colorSend(img, 'red') == CD.red:
            CD.ballColorMatch(img)  # 匹配开舱门
            count = count + 1
        if count > N:
            count = 0
            state = 6
            LED(2).on()
            light.pulse_width_percent(100)  # 打开补光版
            print('red')
            print("state change")
            time.sleep(1)
            LED(2).off()

    elif state == 6:  # 识别绿色，草地，可能需要多声明一个串口信息位，需要补光灯
        if CD.colorSend(img, 'green') == CD.green:
            count = count + 1
        if count > N:
            count = 0
            state = 7
            light.pulse_width_percent(0)  # 关闭补光版
            LED(2).on()
            print('green')
            print("state change")
            time.sleep(1)
            LED(2).off()

    elif state == 7:  # 识别棕色，用户3，是否开舱门
        if CD.colorSend(img, 'brown') == CD.brown:
            CD.ballColorMatch(img)  # 匹配开舱门
            count = count + 1
        if count > N:
            count = 0
            state = 1
            LED(2).on()
            print('brown')
            print("state change")
            time.sleep(1)
            LED(2).off()
    """ ------功能检测------ """
    #CD.colorSend(img, 'blue')
    #CD.colorSend(img, 'green')
    #CD.colorSend(img, 'yellow')
    #CD.colorSend(img, 'red')
    #CD.colorSend(img, 'brown')
    #light.pulse_width_percent(1) # 控制亮度 0~100
    #CD.ballRecog(img)
    """ ------赛道检测------ """
    #pyb.LED(1).on()
    #pyb.LED(2).on()
    #pyb.LED(3).on()
    #CD.ballRecog(img)
    #CD.colorSend(img, 'green')
    print(LD.line_track(img))
    # print(LD.line_track(img))
    """ ------数据发送------ """
    DA.sendData()
    DA.clearData()
    #print(clock.fps()) # 显示FPS
