import pyaudio

call_pin = 2
uno_pin = 4
sim_pin = 17
phone_pin = 27

phone_number = 15570888042

server_IP = '192.168.80.130'
server_port = 8077
server_addr = (server_IP, server_port)
byte_order = '>I'

cache = "cache/"
rate = 44100
channels = 1
format = pyaudio.paInt16
chunk = 1024
rec_seconds = 5
