from smartcard.System import readers
from smartcard.Exceptions import NoCardException
from smartcard.Exceptions import CardConnectionException

#SELECT = [0x00, 0xA4, 0x04, 0x00, 0x0A, 0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01]
#COMMAND = [0x00, 0x00, 0x00, 0x00]
#GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]# get UID command
GET_INF_00 = [0xFF, 0xB0 ,0x00, 0x06, 0x00]
GET_INF_01 = [0xFF, 0xB0 ,0x00, 0x04, 0x00]


class nfcReader:
    def __init__(self):
        self.reader = readers()
        self.connection = None
        self.card = None
        self.uid = None
        self.info = None

    def connect(self):
        try:
            self.connection = self.reader[0].createConnection()
            self.connection.connect()
        
        except NoCardException:
            print("No card found")

        except CardConnectionException:
            print("Card connection error")

        except IndexError:
            print("No reader found")
        
    def get_data(self):
        data01,sw011,sw012 = self.connection.transmit(GET_INF_00)
        data02,sw021,sw022 = self.connection.transmit(GET_INF_01)
        return data01,data02