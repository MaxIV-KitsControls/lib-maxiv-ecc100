import socket
import ecc100_protocol
import ucprotocol
import time
""" receive buffer size (bytes) """
BUFFER_SIZE = 1024

""" line feed characters """
LF = '\n'

TEST_CTAG = 0x99
TIME_DELAY = 0.25

class ECC100():

    def __init__(self, host):
        self.ECC100_HOST = host
        self.ECC100_TCP_PORT = 2101

        self.connect()
        self.disable_events()
        try:
            self.AXIS0_NAME = self.get_name(0).rstrip()
            self.AXIS1_NAME = self.get_name(1).rstrip()
            self.AXIS2_NAME = self.get_name(1).rstrip()
        except Exception as ex:
            self.AXIS0_NAME = ''
            self.AXIS1_NAME = ''
            self.AXIS2_NAME = ''

	for axis in [0, 1, 2]:
	    if self.axis_connected(axis):
  		self.enable_output_relay(axis)

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.connect((self.ECC100_HOST, self.ECC100_TCP_PORT))
        except:
            print 'Connection failed'
            pass

    def open(self):
        self.socket.connect((self.ECC100_HOST, self.ECC100_TCP_PORT))

    def close(self):
        self.socket.close()

    def restart(self):
        self.close()
        time.sleep(0.1)
        self.connect()

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
    def disable_events(self):
        resp = self.query(self.parse_set_telegram(0, ecc100_protocol.ID_ASYNC_EN, 0))
        data = ucprotocol.UcAckTelegram.unpack(resp)

    def get_firmware(self):
        resp = self.query(self.parse_get_telegram(0, ecc100_protocol.ID_ECC_FIRMWARE_REV))
        data = ucprotocol.UcAckTelegram.unpack(resp)
        return hex(data[6])[2:]

    def get_position(self, axis):
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

    def get_reference_position(self, axis):
        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_REFPOSITION))
        data = ucprotocol.UcAckTelegram.unpack(resp)
        return float(data[6])  # unit nm

    def get_reference_position_valid(self, axis):
        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_REFPOS_VALID))
        data = ucprotocol.UcAckTelegram.unpack(resp)
        return data[6]
    
    def enable_movement(self, axis):
        # Controls the approach of the actor to the target position. 1: enable approach, 0: Stop movement
        resp = self.query(self.parse_set_telegram(axis,
                                                  ecc100_protocol.ID_ECC_MOVE_ABS,
                                                  1))
        try:
            data = ucprotocol.UcAckTelegram.unpack(resp)
            result = int(data[5])
        except Exception as ex:
            result = 1

        return result  # check protocol  for error codes, 0: ok

    def disable_movement(self, axis):
        # Controls the approach of the actor to the target position. 1: enable approach, 0: Stop movement
        resp = self.query(self.parse_set_telegram(axis,
                                                  ecc100_protocol.ID_ECC_MOVE_ABS,
                                                  0))
        try:
            data = ucprotocol.UcAckTelegram.unpack(resp)
            result = int(data[5])
        except Exception as ex:
            result = 1

        return result  # check protocol  for error codes, 0: ok

    def enable_output_relay(self, axis):
	# Controls the output relais of the selected axis. 1: on, 0: off
        resp = self.query(self.parse_set_telegram(axis,
                                                  ecc100_protocol.ID_ECC_OUTPUT_EN,
                                                  1))
        try:
            data = ucprotocol.UcAckTelegram.unpack(resp)
            result = int(data[5])
        except Exception as ex:
            result = 1

        return result  # check protocol  for error codes, 0: ok
    
    def disable_output_relay(self, axis):
	# Controls the output relais of the selected axis. 1: on, 0: off
        resp = self.query(self.parse_set_telegram(axis,
                                                  ecc100_protocol.ID_ECC_OUTPUT_EN,
                                                  0))
        try:
            data = ucprotocol.UcAckTelegram.unpack(resp)
            result = int(data[5])
        except Exception as ex:
            result = 1

        return result  # check protocol  for error codes, 0: ok

    def trigger_single_step_backward(self, axis):
        resp = self.query(self.parse_set_telegram(axis,
                                                  ecc100_protocol.ID_ECC_SGL_STEP_BKWD,
                                                  1))
        try:
            data = ucprotocol.UcAckTelegram.unpack(resp)
            result = int(data[5])
        except Exception as ex:
            result = 1

        return result  # check protocol  for error codes, 0: ok

    def trigger_single_step_forward(self, axis):
        resp = self.query(self.parse_set_telegram(axis,
                                                  ecc100_protocol.ID_ECC_SGL_STEP_FWD,
                                                  1))
        try:
            data = ucprotocol.UcAckTelegram.unpack(resp)
            result = int(data[5])
        except Exception as ex:
            result = 1

        return result  # check protocol  for error codes, 0: ok
    
    def trigger_continous_backward(self, axis, cont=1):
        # if cont = 0, stops all movement of the axis regardless its direction.
        resp = self.query(self.parse_set_telegram(axis,
                                                  ecc100_protocol.ID_ECC_CONT_BKWD,
                                                  cont))
        try:
            data = ucprotocol.UcAckTelegram.unpack(resp)
            result = int(data[5])
        except Exception as ex:
            result = 1

        return result  # check protocol  for error codes, 0: ok
   
    def timed_continous_backward(self, axis, delay=0.1):
        self.trigger_continous_backward(axis)
        time.sleep(delay)
        self.trigger_continous_backward(axis, 0)

    def timed_continous_forward(self, axis, delay=0.1):
        self.trigger_continous_forward(axis)
        time.sleep(delay)
        self.trigger_continous_forward(axis, 0)

    def trigger_continous_forward(self, axis, cont=1):
        # if cont = 0, stops all movement of the axis regardless its direction.
        resp = self.query(self.parse_set_telegram(axis,
                                                  ecc100_protocol.ID_ECC_CONT_FWD,
                                                  cont))
        try:
            data = ucprotocol.UcAckTelegram.unpack(resp)
            result = int(data[5])
        except Exception as ex:
            result = 1

        return result  # check protocol  for error codes, 0: ok
    
    def reset_position(self, axis):
        resp = self.query(self.parse_set_telegram(axis, ecc100_protocol.ID_ECC_POSITION_RESET, 1))
        data = ucprotocol.UcAckTelegram.unpack(resp)
        return data[6]

    def axis_connected(self, axis):
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

    def get_on_target_status(self, axis):
        resp = self.query(self.parse_get_telegram(axis, ecc100_protocol.ID_ECC_TARGET_STATUS))
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
