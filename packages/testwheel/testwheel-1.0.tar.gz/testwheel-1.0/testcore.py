import telnetlib


class TelnetClient:
    def __init__(self, ):
        self.tn = telnetlib.Telnet()

    def Telnet(self, IP, username='', password=''):
        """ TODO 设置IP,实现telnet登录主机 """
        self.host_ip = IP
        try:
            self.tn = telnetlib.Telnet(self.host_ip, port=1024)
        except:
            print('%s网络连接失败' % self.host_ip)
            # 等待login出现后输入用户名，最多等待2秒
            return
        self.tn.read_until(b'login: ', timeout=2)
        self.tn.write(username.encode('ascii') + b'\n')
        # 等待Password出现后输入用户名，最多等待2秒
        self.tn.read_until(b'Password: ', timeout=2)
        self.tn.write(password.encode('ascii') + b'\n')
        # 延时两秒再收取返回结果，给服务端足够响应时间
        # 调试
        self.tn.set_debuglevel(2)

    def quit(self):
        """ TODO 退出telnet"""
        self.tn.write(b"exit\n")

    def bindChannel(self, tube):
        """ TODO 通道设置"""
        self.A = tube[0]
        self.B = tube[1]
        self.C = tube[2]
        self.tube1 = bin(int(self.A, 16))[2:].zfill(8)
        self.tube2 = bin(int(self.B, 16))[2:].zfill(6)
        self.D = bin(int(self.C, 16))[2:].zfill(4)
        self.tube3 = self.D[0:2].zfill(2)
        self.tube4 = self.D[2:4].zfill(8)
        self.tube = self.tube1 + self.tube2 + self.tube3 + self.tube4
        print('十位通道：%s' % self.tube)
        return self.tube

    def setChannelTime(self, duration):
        """ TODO 设置通断次数"""
        self.duration = bin(int(duration, 16))[2:].zfill(16)
        return self.duration

    def setclickTime(self, turnon_time, turnoff_time):
        """ TODO 设置单次导通时间和单次关断时间(拆分匹配) """
        self.turnon_time = bin(int(turnon_time, 16))[2:].zfill(16)
        self.turnoff_time = bin(int(turnoff_time, 16))[2:].zfill(16)
        self.Times = self.turnon_time + self.turnoff_time
        return (self.Times)

    def ChannelsInit(self, tube='000000110011111100000011'):
        """ TODO 初始化 """
        W = '00110000'
        command = W + tube
        self.T1 = command
        print(self.T1)
        a = self.T1[0:8]
        a1 = int(a, 2)
        b = self.T1[8:16]
        b1 = int(b, 2)
        c = self.T1[16:24]
        c1 = int(c, 2)
        d = self.T1[24:32]
        d1 = int(d, 2)
        self.T2 = [a1, b1, c1, d1, 0, 0, 0, 0, 0, 0]
        self.T3 = bytes(self.T2)
        print('初始化：', self.T3.hex())
        self.tn.write(self.T3)

    def releaseChannel(self, tube):
        """ TODO 释放通道 """
        # 执行命令
        W = '00110000'
        command = W + tube
        self.release_cmd = command
        self.excute(self.release_cmd, 32)

    def setChannelRun(self, tube, Times, duration):
        """ TODO 通道运行  """
        # 执行命令
        W = '00110001'
        command = W + tube + Times + duration
        self.setRun_cmd = command
        self.excute(self.setRun_cmd, 80)

    def setChannelOn(self, tube):
        """ TODO 通道打开 """
        # 执行命令
        W = '00110001'
        Q = '00000011110010000000000000000000'
        D = bin(int('0000', 16))[2:].zfill(16)
        command = W + tube + Q + D
        self.setOn_cmd = command
        self.excute(self.setOn_cmd, 80)
        A2 = self.tn.read_very_eager().hex()
        A = str(self.tn.read_until(b"\n", timeout=2).hex())
        print('打开通道的返回值：', A[:-2])

    def setChannelOff(self, tube):
        """ TODO 通道关闭 """
        # 执行命令
        W = '00110000'
        Q = '00000000000000000000001111001000'
        D = bin(int('0000', 16))[2:].zfill(16)
        command = W + tube + Q + D

        self.setOff_cmd = command
        self.excute(self.setOff_cmd, 80)
        A2 = self.tn.read_very_eager().hex()
        A = str(self.tn.read_until(b"\n", timeout=2).hex())
        print('打开通道的返回值：', A[:-2])

    def excute(self, command, num):
        ''' TODO 通用执行模板 '''
        self.cmd = command
        print('要执行的模板命令：', self.cmd)
        self.cmd_list = []
        for i in range(0, num, 8):
            x = int(self.cmd[i:i + 8], 2)
            self.cmd_list.append(x)
        if len(self.cmd_list) == 4:
            self.cmd_list.extend([0, 0, 0, 0, 0, 0])
        print('----------------------------')
        print('写入前模板的十进制：', self.cmd_list)
        self.cmd_listTOBytes = bytes(self.cmd_list)
        print('将模板列表转字节串：', self.cmd_listTOBytes.hex())
        print('----------------------------')
        self.tn.write(self.cmd_listTOBytes)
