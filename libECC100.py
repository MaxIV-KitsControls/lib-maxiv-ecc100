import socket
import ecc100_protocol
import ucprotocol
import time
""" receive buffer size (bytes) """
BUFFER_SIZE = 1024

""" line feed characters """
LF = '\n'

TEST_CTAG = 0x99


class ECC100():

    def __init__(self, host):
        self.ECC100_HOST = host
        self.ECC100_TCP_PORT = 2101

        self.connect()

        try:
            self.AXIS0_NAME = self.get_name(0).rstrip()
            self.AXIS1_NAME = self.get_name(1).rstrip()
            self.AXIS2_NAME = self.get_name(1).rstrip()
        except Exception as ex:
            self.AXIS0_NAME = ''
            self.AXIS1_NAME = ''
            self.AXIS2_NAME = ''

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.connect((self.ECC100_HOST, self.ECC100_TCP_PORT))
        except:
            print 'Connection failed'
            pass

    def open(self, host, port):
        self.sockect.connect((self.ECC100_HOST, self.ECC100_TCP_PORT))

    def close(self):
        self.socket.close()

    def restart(self):
        self.close()
        self.open()

    def send(self, cmd):
        self.socket.send(cmd + LF)

    def recv(self):
        r = self.socket.recv(BUFFER_SIZE).rstrip(LF)
        return r

    def query(self, cmd):
        try:
            self.socket.sendall(cmd)  # or perhaps plain send?
            return self.recv()
        except ValueError as err:
            raise ValueError("Command type error: %s" % str(err))

    def parse_get_telegram(self, axis, address):
        return ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                             ucprotocol.UC_GET,
                                             address,
                                             axis,
                                             TEST_CTAG)

    def parse_set_telegram(self, axis, address, value):
        return ucprotocol.UcSetTelegram.pack(ucprotocol.UcSetTelegram_size,
                                             ucprotocol.UC_SET,
                                             address,
                                             axis,
                                             TEST_CTAG,
                                             value)

    def get_firmware(self):
        resp = self.query(self.parse_get_telegram(0, ecc100_protocol.ID_ECC_FIRMWARE_REV))
        data = ucprotocol.UcAckTelegram.unpack(resp)
        return hex(data[6])[2:]

    def get_position(self, axis):
        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_POSITION))
        try:
            data = ucprotocol.UcAckTelegram.unpack(resp)
        except Exception as ex:
            resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_POSITION))
            data = ucprotocol.UcAckTelegram.unpack(resp)

        return float(data[6])  # unit nm

    def set_position(self, axis, position):
        resp = self.query(self.parse_set_telegram(axis,
                                                  ecc100_protocol.ID_ECC_TARGET_POS,
                                                  position))
        try:
            data = ucprotocol.UcAckTelegram.unpack(resp)
            result = int(data[5])
        except Exception as ex:
            result = 1

        return result  # check protocol  for error codes, 0: ok

    def axis_connected(self, axis):
        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_CONNECTED))
        try:
            data = ucprotocol.UcAckTelegram.unpack(resp)
        except:
            resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_CONNECTED))
            data = ucprotocol.UcAckTelegram.unpack(resp)

        return data[6]

    def get_moving_status(self, axis):
        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_MOVING))
        data = ucprotocol.UcAckTelegram.unpack(resp)
        return data[6]

    def get_end_of_travel_forward(self, axis):
        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_EOT_FWD))
        data = ucprotocol.UcAckTelegram.unpack(resp)
        return data[6]

    def get_end_of_travel_backward(self, axis):
        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_EOT_BKWD))
        data = ucprotocol.UcAckTelegram.unpack(resp)
        return data[6]

    def get_name(self, axis):
        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_AXIS_MOTORNAME_0))
        name0 = hex(ucprotocol.UcAckTelegram.unpack(resp)[6])[2:].decode('hex')

        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_AXIS_MOTORNAME_1))
        name1 = hex(ucprotocol.UcAckTelegram.unpack(resp)[6])[2:].decode('hex')

        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_AXIS_MOTORNAME_2))
        name2 = hex(ucprotocol.UcAckTelegram.unpack(resp)[6])[2:].decode('hex')

        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_AXIS_MOTORNAME_3))
        name3 = hex(ucprotocol.UcAckTelegram.unpack(resp)[6])[2:].decode('hex')

        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_AXIS_MOTORNAME_4))
        name4 = hex(ucprotocol.UcAckTelegram.unpack(resp)[6])[2:].decode('hex')
        return name4+name3+name2+name1+name0  # this is wonderful...


def test():
    host_list = ['172.16.118.51', '172.16.118.53', '172.16.118.52']

    positions = [600, 1200, 1800]  # [nm]

    print 'Starting test program...'
    for host in host_list:
        print 'Controller host: ', host
        ecc100 = ECC100(host=host)

        print 'connected axis names: ', ecc100.AXIS0_NAME, ecc100.AXIS1_NAME, ecc100.AXIS2_NAME
        print 'AXIS 0 >>> Position: ', ecc100.get_position(0), '| Connected: ', ecc100.axis_connected(0)
        print 'AXIS 1 >>> Position: ', ecc100.get_position(1), '| Connected: ', ecc100.axis_connected(1)
        print 'AXIS 2 >>> Position: ', ecc100.get_position(2), '| Connected: ', ecc100.axis_connected(2)

        ecc100.close()
        print 'Connection closed'
        print '#################\n'
        time.sleep(0.5)

    print '$$$$$$$$$$$\n'
    print 'Moving to new positions...'
    for host in host_list:
        try:
            print 'Controller host: ', host
            ecc100 = ECC100(host=host)
            try:
                ecc100.set_position(0, positions[0])
            except:
                print 'error axis 0'
            try:
                ecc100.set_position(1, positions[1])
            except:
                print 'error axis 1'
            try:
                ecc100.set_position(2, positions[2])
            except:
                print 'error axis 2'

            time.sleep(0.1)

            try:
                print 'AXIS 0 >>> Position: ', ecc100.get_position(0)
            except:
                print 'error getting axis'
            time.sleep(0.1)

            try:
                print 'AXIS 1 >>> Position: ', ecc100.get_position(1)
            except:
                print 'error getting axis'
            time.sleep(0.1)

            try:
                print 'AXIS 2 >>> Position: ', ecc100.get_position(2)
            except:
                print 'error getting axis'
            
            ecc100.close()
            print 'Connection closed'
            print '#################\n'

            time.sleep(0.5)

        except Exception as ex:
            ecc100.close()
            print 'Setting error!! ',ex
            time.sleep(0.5)

    print 'Test finished'
    print '#################\n'

if __name__ == '__main__':
    test()
