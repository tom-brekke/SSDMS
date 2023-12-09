#!/usr/bin/env python
from __future__ import print_function
import sys
import time
import argparse
import pyaudio
import numpy as np
import datetime

#this script should be executed when you want to begin monitoring for dog barks


parser=argparse.ArgumentParser()
parser.add_argument("--time", type=int, required=False, help="time in seconds to monitor the sausage dog, default 24 hours", default=10)


args=parser.parse_args()
time=args.time



CHUNK = 2**11
RATE = 8000
CHANNELS = 1
p=pyaudio.PyAudio()

stream=p.open(format=pyaudio.paInt16, rate=RATE, channels=1, input=True, frames_per_buffer=CHUNK)

'''
for i in range(int(time*234/60)): 
	data = np.fromstring(stream.read(CHUNK,  exception_on_overflow = False ),dtype=np.int16)
	peak=np.average(np.abs(data))*2
	bars="#"*int(50*peak/2**16)
	print("%04d %05d %s"%(i,peak,bars), file=sys.stdout)
	if peak >4000:
		if sendto:
			SendEmail(sendto, subject, body, attachment)
	if outfile:
		now = datetime.datetime.now()
		print(peak, now.strftime("%Y-%m-%d %H:%M"), file=OUT)
'''
stream.stop_stream()
stream.close()
p.terminate()

