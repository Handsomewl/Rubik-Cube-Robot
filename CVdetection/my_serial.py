import serial
import numpy as np

class Ser(object):
    def __init__(self, com):
        #打开端口
        self.port = serial.Serial(com, 9600, timeout=0)

    def send_cmd(self, cmd):
        cmd_ascii = np.fromstring(cmd, dtype=np.uint8)
        write_num = self.port.write(cmd_ascii)

        #self.port.flush()

        return write_num

    def readall(self):
        return self.port.readall().decode()

    def read(self, num):
        return self.port.read(num)

    def get_in_waiting(self):
        return self.port.in_waiting

    def get_out_waiting(self):
        return self.port.out_waiting

    def flush(self):
        self.port.flush()

    def close(self):
        self.port.close()