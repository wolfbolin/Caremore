import pyaudio

cache = "cache/"
rate = 44100
channels = 1
format = pyaudio.paInt16
chunk = 1024
rec_seconds = 5