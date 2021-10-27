import sensor, image, time
import colorDef as CD
import lineDef as LD

"""    初始化openmv摄像头模块     """
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()  # Create a clock object to track the FPS.
"""    定义狗子状态    """

"""    主循环    """
while (True):
    clock.tick()  # Update the FPS clock.
    # img = sensor.snapshot()  # Take a picture and return the image.

    sensor.set_pixformat(sensor.RGB565)
    img = sensor.snapshot()


    #CD.colorRecog(img, 'brown', CD.color_threshold)
    #CD.colorRecog(img, 'red', CD.color_threshold)
    #CD.colorRecog(img, 'green', CD.color_threshold)
    #CD.colorRecog(img, 'yellow', CD.color_threshold)
    CD.colorRecog(img, 'blue', CD.blue, CD.color_threshold)

    #a = LD.line_track(img, LD.grayLine)
    #time.sleep_ms(10)
    #print(a)
    #print(clock.fps())
