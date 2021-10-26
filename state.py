class State:
    # 定义状态
    def __init__(self):
        """Initialize"""

        # 识别球后的状态变量定义
        self.Ball = 0  # 拿球为1，没球为0
        self.User = 0  # 用户123 1：黑+绿，2：黑+紫红，3：黑+棕

        # 赛道标识符
        """通用符号"""
        self.Black = 0  # 识别黑道前为0，识别后为1
        """集散区，起点区"""
        self.Blue = 0  # 识别蓝色前为0，识别后为1
        """用户区"""
        self.Green = 0  # 1号用户
        self.Red = 0  # 2号用户
        self.Brown = 0  # 3号用户
        """赛道通用区"""
        self.Yellow = 0  # 上台阶 黄色为1
        self.Bridge = 0  # 台阶后窄桥 无颜色标识
        self.SpecialRed = 0  # 窄桥后下台阶 识别黄色后再启用，放置与2号用户冲突
        """赛道特殊部分区"""
        self.Deceleration = 0  # 减速带无颜色
        self.Grass = 0  # 草地前无黑带，绿色为1

    def state_init(self):
        """来到起点后的初始化
        """
        self.Ball = 0
        self.User = 0
        self.Black = 0
        self.Blue = 0
        self.Green = 0
        self.Red = 0
        self.Brown = 0
        self.Yellow = 0
        self.Bridge = 0
        self.SpecialRed = 0
        self.Deceleration = 0
        self.Grass = 0

    def getBall(self, user):
        """拿到球，定位用户

        Args:
            user (类型未定): 几号用户，123
        """
        self.Ball = 1
        self.User = user

    def colorFlag(self, color):
        if color == 1:
            return True
        else:
            return False
