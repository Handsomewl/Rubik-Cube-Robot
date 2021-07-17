import my_serial
import time


str_solution = 'R2F1D1F3L2F1B3L1D1R3F2R3L1U3D2B1F3L2R3'

print(str_solution)

x=1
print(x)
#端口发送
ser = my_serial.Ser('com10')

ser.send_cmd(str_solution+'#')
time.sleep(0.5)

flag = True
while(flag):
    if ser.get_in_waiting():
        print(ser.read(2))
        flag = False
    else:
        ser.send_cmd(str_solution+'#')
        x += 1
        print(x)
        time.sleep(0.5)

time.sleep(3)
print(ser.readall())

ser.close()