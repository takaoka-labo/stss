from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.CardConnection import CardConnection
from smartcard.Exceptions import NoCardException
from smartcard.Exceptions import CardConnectionException

#SELECT = [0x00, 0xA4, 0x04, 0x00, 0x0A, 0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01]
#COMMAND = [0x00, 0x00, 0x00, 0x00]
#GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]# get UID command
#GET_INF_00 = [0xFF, 0xB0 ,0x00, 0x00, 0x00] #CLA, INS, P1, P2, Le

#タグのNFC Toolsによるテキスト書き込み : "   i,str," <- (i : NFC_TYPE, str : content)
#スペース3つ先頭、カンマ区切り
#これで 7ブロック読み取り開始でちょうどiから読み取れる
GET_INF_01 = [0xFF, 0xB0 ,0x00, 0x07, 0x00]

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
            #print("No card found")
            return False

        except CardConnectionException:
            #print("Card connection error")
            return False

        except IndexError:
            #print("No reader found")
            return False
        else:
            return True

    def get_data(self):
        #data01,sw011,sw012 = self.connection.transmit(GET_INF_00)
        data02,sw021,sw022 = self.connection.transmit(GET_INF_01)

        #print(toHexString(data01))
        #print('---')
        #print(toHexString(data02))

        #data_size = data01[1] - 6
        extracted_bytes = data02[0:]
        #print(toHexString(extracted_bytes))
        ascii_chars = [chr(byte) for byte in extracted_bytes]

        string = ''.join(ascii_chars)
        #print(string)
        tmp = string.split(',')
        print(tmp)
        NFC_TYPE = int(tmp[0])
        print('temp[1] = ',tmp[1])
        return NFC_TYPE,tmp[1]