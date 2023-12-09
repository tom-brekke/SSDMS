#!/usr/bin/env python

import pyaudio
import numpy as np

CHUNK = 2**11
RATE = 8000
CHANNELS = 1
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16, rate=RATE, channels=1, input=True, frames_per_buffer=CHUNK)

for i in range(int(10*8000/1024)): #go for a few seconds
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    bars="#"*int(50*peak/2**16)
    print("%04d %05d %s"%(i,peak,bars))
    if (peak >4000):
            #take_picture
            #send_email
stream.stop_stream()
stream.close()
p.terminate()

