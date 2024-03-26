import stss_motor

stss_motor.mySTS.DEVICENAME = '/dev/ttyUSB0'
stss_motor.mySTS.prepare_STS()

servo = stss_motor.revolver(1,1000000)
for i in range(6):
    servo.position(i)

stss_motor.mySTS.close()