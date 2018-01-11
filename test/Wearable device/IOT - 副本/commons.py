import pyaudio

phone_number = 15570888042

byte_order = '>I'
server_IP = '127.0.0.1'
server_port = 8099
server_addr = (server_IP, server_port)

RATE = 44100
CHANNELS = 1
FORMAT = pyaudio.paInt16
DEVICE = None
CHUNK = 1024
RECORD_SECONDS = 10
CACHE = "cache/"

APP_ID = '10293975'
API_KEY = '9VMgabQopDlENZRdmVWiEQrG'
SECRET_KEY = 'fa41369db9ecc04e6fa3a6a92804e61e'

call_pin = 2
uno_pin = 3
sim_pin = 4
phone_pin = 17
