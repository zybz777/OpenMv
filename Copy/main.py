# 主函数 - By: zyb - 周一 10月 25 2021
import sensor, image, time
import colorDef as CD
import lineDef as LD
import data as DA
import pyb

from pyb import Pin, Timer, LED
import time
"""    初始化openmv     """
LED(2).on()  # openmv启动标志
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
N = 3  # count 比较数值
sleep_time = 2  # 全局延迟时间，每个状态切换之间给狗子行走的时间，防止将当前颜色识别成下一状态颜色
flag_grass = 0
print("begin")
print("now is state 1")
LED(2).off()  # openmv启动完成
"""    主循环    """
while True:
    clock.tick()
    img = sensor.snapshot()
    """ ------颜色检测------- """
    #"""
    if state == 1:  # 识别蓝色，准备装载小球
        if CD.colorSend(img, 'blue') == CD.blue:
            count += 1  # 串口发送数据+1
        # 状态转换
        if count > N:
            count = 0
            CD.ballColor = 0
            state = 2
            print("now is state 2")
            LED(2).on()  # 状态切换标志
            time.sleep(sleep_time)
            LED(2).off()
            light.pulse_width_percent(1)

    elif state == 2:  # 小球判断
        CD.ballRecog(img)
        if CD.ballColor != 0:  # 识别到小球
            count += 1  # 串口发送数据+1
        # 状态转换
        if count > 1:
            state = 3
            #if CD.ballColor == CD.green:
            #time.sleep(3)
            print("now is state 3")
            light.pulse_width_percent(0)
            LED(2).on()
            time.sleep(sleep_time)
            LED(2).off()

    elif state == 3:  # 识别绿色，用户1，是否开舱门
        if CD.colorSend(img, 'green') == CD.green:
            if CD.ballColor == CD.green:
                CD.ballColorMatch()  # 匹配开舱门
            count += 1
        # 状态转换
        if count > N:
            count = 0
            state = 4
            print("now is state 4")
            LED(2).on()
            time.sleep(4)
            LED(2).off()

    elif state == 4:  # 识别黄色，上台阶
        if CD.colorSend(img, 'yellow') == CD.yellow:
            count += 1
        # 状态转换
        if count > N:
            count = 0
            state = 5
            print("now is state 5")
            LED(2).on()
            time.sleep(1)
            LED(2).off()

    elif state == 5:  # 识别红色，用户2，是否开舱门，且下斜坡
        if CD.colorSend(img, 'red') == CD.red:
            if CD.ballColor == CD.red:
                CD.ballColorMatch()  # 匹配开舱门
            count += 1
        # 状态转换
        if count > N:
            count = 0
            state = 6
            print("now is state 6")
            LED(2).on()
            time.sleep(1)
            LED(2).off()
            light.pulse_width_percent(100)  # 打开补光版，草地用

    elif state == 6:  # 识别绿色，草地, 执行动作需要改为识别到棕色，然后进入下一状态，这一状态中的任务是 巡线直走
        if flag_grass == 0 and CD.colorSend(img, 'green') == CD.green:
            flag_grass = 1
        elif flag_grass == 1 and CD.colorSend(img, 'green') != CD.green:
            light.pulse_width_percent(0)  # 关闭补光版
            count = 0
            state = 7
            flag_grass = 0
            print("now is state 7")
            LED(2).on()
            time.sleep(1)
            LED(2).off()

    elif state == 7:  # 识别棕色，用户3，是否开舱门
        if CD.colorSend(img, 'brown') == CD.brown:
            if CD.ballColor == CD.brown:
                CD.ballColorMatch()  # 匹配开舱门
            count += 1
        # 状态转换
        if count > N:
            count = 0
            state = 1
            print("now is state 7")
            LED(2).on()
            time.sleep(1)
            LED(2).off()
    #"""
    """ ------功能检测------ """
    #light.pulse_width_percent(100)
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
    #LD.line_track(img.copy())
    # print(LD.line_track(img))
    """ ------数据发送------ """
    DA.sendData()
    DA.clearData()
    #print(clock.fps()) # 显示FPS
