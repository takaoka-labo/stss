if __name__ == "__main__":
    import mySTS
else:
    from . import mySTS
import time

# parameter for revolver
revolver_pos = [0,682,1365,2047,2730,3412]
renolver_pos_offset = 120
revolver_acc = 50
revolver_speed = 6000
position_time = 2 # [s]

# parameter for door
gear_ratio = 6.444
door_move_angle = 60
door_acc = 0
door_close_speed = int(door_move_angle * gear_ratio / 360 * 4096) # 1[s]で移動するposition数
#print(door_close_speed)
door_move_time = 1 # 1[s]
# speed > 0 : close

def setting(DEVICE_NAME):
    mySTS.DEVICENAME = DEVICE_NAME
    mySTS.prepare_STS()

def close():
    mySTS.close()

class revolver:
    def __init__(self,ID,baudrate):
        self.STS = mySTS.mySTS(ID,baudrate)
        self.STS.wheelmode(0)
        self.position(0)

    def position(self,num):
        self.STS.move_absolute_pos(revolver_acc,revolver_speed,revolver_pos[num] + renolver_pos_offset)
        time.sleep(position_time)

class door:
    state = True # True:close False:open

    def __init__(self,ID,baudrate):
        self.STS = mySTS.mySTS(ID,baudrate)
        self.STS.wheelmode(1)
    
    def open(self):
        if self.state == True:
            print('door open')
            self.STS.move_speed(door_acc,-door_close_speed)
            time.sleep(1)
            self.STS.move_speed(door_acc,0)
            time.sleep(1)
            self.state = False
    
    def close(self):
        if self.state == False:
            print('door close')
            self.STS.move_speed(door_acc,door_close_speed)
            time.sleep(1)
            self.STS.move_speed(door_acc,0)
            time.sleep(1)
            self.state = True


if __name__ == "__main__":
    setting('/dev/ttyUSB0')

    
    servo = revolver(1,1000000)
    for i in range(6):
        servo.position(i)
    
    servo2 = door(2,1000000)
    servo2.open()
    time.sleep(1)
    servo2.close()

    close()