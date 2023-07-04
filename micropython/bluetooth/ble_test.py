from ubluetooth import BLE
import ubluetooth
from machine import Pin

led=Pin(2, Pin.OUT)

ble = BLE()
ble.active(True)
led.on()

def ad():
	ble.gap_advertise(100,
		   adv_data=b'\x02\x01\x03\x0b\x09\x65\x73\x70\x33\x32\x5f\x74\x65\x73\x74',
		   resp_data=b'\x02\xff\x12')


def ble_irq(event, data):
	if 1 == event:
		led.off()
		
	elif 2 == event:
		led.on()
		ad()
	
	elif 3 == event:
		conn_hdl, char_hdl = data
		buffer = ble.gatts_read(char_hdl)
		print(buffer)
		if buffer == b'A':
			ble.gatts_notify(0, char_hdl, b'B')
		

ble.irq(ble_irq)

# create uuids
service_1_uuid = ubluetooth.UUID(0x9011)
char_1_uuid = ubluetooth.UUID(0x9012)
char_2_uuid = ubluetooth.UUID(0x9013)
service_2_uuid = ubluetooth.UUID(0x9021)
char_3_uuid = ubluetooth.UUID(0x9022)
# create chars
char1=(char_1_uuid, ubluetooth.FLAG_READ)
char2=(char_2_uuid, ubluetooth.FLAG_READ | ubluetooth.FLAG_WRITE | ubluetooth.FLAG_NOTIFY)
char3=(char_3_uuid, ubluetooth.FLAG_NOTIFY | ubluetooth.FLAG_WRITE)
# create services
service1 = (service_1_uuid, (char1, char2))
service2 = (service_2_uuid, (char3,))
# service set
serv_set = (service1, service2)
# register service
ble.gatts_register_services(serv_set)

ad()

