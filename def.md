# OpenMv函数汇总

Author: ZYB
Date: 2021-10-16

+ Sensor 摄像头模块
    1. `import sensor`
    2. `sensor.reset()` # 初始化摄像头
    3. `sensor.set_pixformat(pixformat)` # 设置像素格式
        pixformat参数：
            `sensor.GRAYSCAL`：灰度图像，每像素 8 位（1 字节），处理速度快；
            `sensor.RGB565`: 每像素为 16 位（2 字节），5 位用于红色，6 位用于绿色，5 位用于蓝色，处理速度比灰度图像要慢。
    4. `sensor.set_framesize(framesize)` # 设置每帧大小
        framesize参数：
            `sensor.QQVGA`: 160*120;
            `sensor.QVGA`: 320*240; 常用
            `sensor.VGA`: 640*480;
        > 用于LCD模块的参数请查询手册
    5. `sensor.skip_frames([n, time])` # n 和 time 均没指定，默认跳过 300 毫秒的帧
    6. `sensor.snapshot()` # 使用相机拍摄一张照片，并返回 image 对象。
    7. `sensor.set_auto_gain(False)` # 关闭自动增益
    8. `sensor.set_auto_whitebal(False)` # 关闭白平衡
+ Image 图像模块
