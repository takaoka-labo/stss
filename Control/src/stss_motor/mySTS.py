import os
import sys, tty, termios
sys.path.append(os.pardir)

if __name__ == "__main__":
    from scservo_sdk import *                # Uses SCServo SDK library
else:
    from .scservo_sdk import *

# Control table address
ADDR_SCS_TORQUE_ENABLE     = 40
ADDR_SCS_GOAL_ACC          = 41
ADDR_SCS_GOAL_POSITION     = 42
ADDR_SCS_GOAL_SPEED        = 46
ADDR_SCS_PRESENT_POSITION  = 56

ADDR_SCS_MODE = 33

if os.name == 'nt':
        import msvcrt
        def getch():
            return msvcrt.getch().decode()
else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        def getch():
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
        
DEVICENAME = ""    # define in your code
portHandler = None
packetHandler = None

def prepare_STS():
    global portHandler,packetHandler
    protocol_end = 0                 # SCServo bit end(STS/SMS=0, SCS=1)
    
    # Initialize PortHandler instance
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    portHandler = PortHandler(DEVICENAME)

    # Initialize PacketHandler instance
    # Get methods and members of Protocol
    packetHandler = PacketHandler(protocol_end)

    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()

class mySTS:
    global portHandler,packetHandler
    def __init__(self,sts_id,baudrate):
        self.SCS_ID = sts_id
        self.Baudrate = baudrate

        # Open port
        if portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            quit()

        # Set port baudrate
        if portHandler.setBaudRate(self.Baudrate):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()

        # Try to ping the SCServo
        # Get SCServo model number
        scs_model_number, scs_comm_result, scs_error = packetHandler.ping(portHandler, self.SCS_ID)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))
        else:
            print("[ID:%03d] ping Succeeded. SCServo model number : %d" % (self.SCS_ID, scs_model_number))
    
    def wheelmode(self,mode):
        scs_comm_result, scs_error = packetHandler.write1ByteTxRx(portHandler, self.SCS_ID, ADDR_SCS_MODE, mode)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))

    def move_absolute_pos(self,acc,speed,position):
        # Write SCServo acc
        scs_comm_result, scs_error = packetHandler.write1ByteTxRx(portHandler, self.SCS_ID, ADDR_SCS_GOAL_ACC, acc)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))

        # Write SCServo speed
        scs_comm_result, scs_error = packetHandler.write2ByteTxRx(portHandler, self.SCS_ID, ADDR_SCS_GOAL_SPEED, speed)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))

        # Write SCServo goal position
        scs_comm_result, scs_error = packetHandler.write2ByteTxRx(portHandler, self.SCS_ID, ADDR_SCS_GOAL_POSITION, position)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))
    
    def move_speed(self,acc,speed):
        # Write SCServo acc
        scs_comm_result, scs_error = packetHandler.write1ByteTxRx(portHandler, self.SCS_ID, ADDR_SCS_GOAL_ACC, acc)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))

        _speed_ = speed
        
        # Write SCServo speed
        if speed<0 :
            _speed_ = -speed
            print(_speed_)
            print(_speed_.to_bytes(2))
            _speed_ |= (1<<15)
        
        scs_comm_result, scs_error = packetHandler.write2ByteTxRx(portHandler, self.SCS_ID, ADDR_SCS_GOAL_SPEED, _speed_)
        print(_speed_)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))

def close():
    global portHandler,packetHandler
    # Close port
    portHandler.closePort()

if __name__ == "__main__":
    import mySTS,time

    DEVICENAME = '/dev/ttyUSB0'
    prepare_STS()

    servo = mySTS(1,1000000)
    servo.wheelmode(1)
    #servo.move_absolute_pos(100,1000,0) #0.acceralation 1.speed 2.position
    servo.move_speed(100,4096) #0.acceralation 1.speed
    time.sleep(1)
    servo.move_speed(50,0) #0.acceralation 1.speed
    close()