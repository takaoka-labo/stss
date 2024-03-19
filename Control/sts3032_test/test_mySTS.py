import mySTS,time

mySTS.DEVICENAME = '/dev/ttyUSB0'
mySTS.prepare_STS()

servo = mySTS.mySTS(1,1000000)
servo.wheelmode(1)
#servo.move_absolute_pos(100,1000,0) #0.acceralation 1.speed 2.position
servo.move_speed(50,1000) #0.acceralation 1.speed
time.sleep(1)
servo.move_speed(50,0) #0.acceralation 1.speed
mySTS.close()