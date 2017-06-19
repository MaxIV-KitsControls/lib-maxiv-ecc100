import demo
import ucprotocol
import ecc100_protocol
import time
import sys

TEST_CTAG = 0x99
ECC100_HOST = '172.16.118.52'
# '172.16.118.52'
# '172.16.118.51'  Axis 1

ecc100 = demo.ECC100(sys.argv[1])
ecc100.connect()

if len(sys.argv) == 3:
    ACTOR = int(sys.argv[2])
else:
    ACTOR = 0  # this is the axis: 0, 2, 1

uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_FIRMWARE_REV,
                                         0,
                                         TEST_CTAG)


resp = ecc100.query(uc_get_telegram)
data = ucprotocol.UcAckTelegram.unpack(resp)
print 'ACTOR: ', ACTOR
print 'Firmware: ', hex(data[6])[2:]
time.sleep(0.1)

# ecc100.close()

# ecc100.connect(host= sys.argv[1])

uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_POSITION,
                                         ACTOR,
                                         TEST_CTAG)
resp = ecc100.query(uc_get_telegram)
data = ucprotocol.UcAckTelegram.unpack(resp)
print 'Position: ', data[6], ' nm'
time.sleep(0.1)

# ecc100.close()
# ecc100.connect(host= sys.argv[1])

uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_REFPOSITION,
                                         ACTOR,
                                         TEST_CTAG)

resp = ecc100.query(uc_get_telegram)
data = ucprotocol.UcAckTelegram.unpack(resp)
print 'Reference Position: ', data[6], ' nm'
time.sleep(0.1)

uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_TARGET_POS,
                                         ACTOR,
                                         TEST_CTAG)

resp = ecc100.query(uc_get_telegram)
data = ucprotocol.UcAckTelegram.unpack(resp)
print 'Target Position: ', data[6],' nm'
time.sleep(0.1)

uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_CONNECTED,
                                         ACTOR,
                                         TEST_CTAG)

resp = ecc100.query(uc_get_telegram)
data = ucprotocol.UcAckTelegram.unpack(resp)
print 'Sensor Connected?: ', data[6]

uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_AMPL,
                                         ACTOR,
                                         TEST_CTAG)
resp = ecc100.query(uc_get_telegram)
data = ucprotocol.UcAckTelegram.unpack(resp)
print 'Amplitude: ', data[6]
time.sleep(0.1)

uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_FREQ,
                                         ACTOR,
                                         TEST_CTAG)
resp = ecc100.query(uc_get_telegram)
data = ucprotocol.UcAckTelegram.unpack(resp)
print 'Frequency: ', data[6]
time.sleep(0.1)

uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_ACTOR_SEL,
                                         ACTOR,
                                         TEST_CTAG)
resp = ecc100.query(uc_get_telegram)
data = ucprotocol.UcAckTelegram.unpack(resp)
print 'Actor selected: ', data[6]
time.sleep(0.1)

uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_AXIS_TYPE,
                                         ACTOR,
                                         TEST_CTAG)
resp = ecc100.query(uc_get_telegram)
data = ucprotocol.UcAckTelegram.unpack(resp)
print 'Actor type: ', data[6]
time.sleep(0.1)

uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_AXIS_MOTORNAME_0,
                                         ACTOR,
                                         TEST_CTAG)
resp = ecc100.query(uc_get_telegram)
name0 = hex(ucprotocol.UcAckTelegram.unpack(resp)[6])[2:].decode('hex')
uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_AXIS_MOTORNAME_1,
                                         ACTOR,
                                         TEST_CTAG)
resp = ecc100.query(uc_get_telegram)
name1 = hex(ucprotocol.UcAckTelegram.unpack(resp)[6])[2:].decode('hex')
uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_AXIS_MOTORNAME_2,
                                         ACTOR,
                                         TEST_CTAG)
resp = ecc100.query(uc_get_telegram)
name2 = hex(ucprotocol.UcAckTelegram.unpack(resp)[6])[2:].decode('hex')
uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_AXIS_MOTORNAME_3,
                                         ACTOR,
                                         TEST_CTAG)
resp = ecc100.query(uc_get_telegram)
name3 = hex(ucprotocol.UcAckTelegram.unpack(resp)[6])[2:].decode('hex')
uc_get_telegram = ucprotocol.UcGetTelegram.pack(ucprotocol.UcGetTelegram_size,
                                         ucprotocol.UC_GET,
                                         ecc100_protocol.ID_ECC_AXIS_MOTORNAME_4,
                                         ACTOR,
                                         TEST_CTAG)
resp = ecc100.query(uc_get_telegram)
name4 = hex(ucprotocol.UcAckTelegram.unpack(resp)[6])[2:].decode('hex')
print 'Name: ', name4+name3+name2+name1+name0

ecc100.close()