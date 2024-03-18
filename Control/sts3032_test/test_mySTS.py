import mySTS

mySTS.DEVICENAME = '/dev/ttyUSB0'
mySTS.prepare_STS()

servo = mySTS.mySTS(1,1000000)
servo.move_absolute(100,1500,4000) #0.acceralation 1.speed 2.position

mySTS.close()
