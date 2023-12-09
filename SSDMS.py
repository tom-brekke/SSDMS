#!/usr/bin/env python
from __future__ import print_function
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import time
import argparse
import pyaudio
import numpy as np
import datetime
import re

#this script should be executed when you want to begin monitoring for dog barks


parser=argparse.ArgumentParser()
parser.add_argument("--to", "-t", type=str, required=False, help="The recipient's email address, if this is omitted, no email will be sent")
parser.add_argument("--subject", "-s", type=str, default="BARK", required=False, help="The subject line of the email in quotes, only used if --to is called")
parser.add_argument("--body", "-b", type=str, required=False, default="", help="The body text of the email in quotes, only used if --to is called")
parser.add_argument("--fromEmail", "-t", type=str, required=True, help="The senders's email address")
parser.add_argument("--passwd", "-t", type=str, required=True, help="The sender's email password")
parser.add_argument("--attachment", "-a", type=str, required=False, default="", help="The name of the file to attach, only used if --to is called")
parser.add_argument("--time", type=int, required=False, help="time in minutes to monitor the sausage dog, default: 1435 (24 hours = 1440 minutes)", default=1435)
parser.add_argument("--data", type=str, required=False, help="the file to write the data to. Filename will be preceded by the current date if the time is set to default of 1435 minutes (i.e. just shy of 24 hours which would be 1440)")
parser.add_argument("--threshhold", type=int, required=False, help="the threshold that will trigger an email - 2500 is standard quiet house, >15000 is loud barking, default: 15000", default=15000)


args=parser.parse_args()
sendto=args.to
subject=args.subject
body=args.body
attachment=args.attachment
time=args.time
threshhold=args.threshhold
outfile=args.data
if outfile:
	if time==1435:	#1400 is default
		today = datetime.datetime.now().strftime("%Y-%m-%d")
		if re.search("/", outfile):
			outfileParts=outfile.split("/")
			outfileParts[-1]=today+"_"+outfileParts[-1]
			outfile="/".join(outfileParts)
		else:
			outfile=today+"_"+outfile
	OUT=open(outfile, "w")


def SendEmail(sendto, subject, body, attachment, user, passwd):
	msg=MIMEMultipart()
	part=MIMEText(body)#body of email
	msg.attach(part)
	msg['To']=sendto
	msg['From']=user
	msg['Subject']=subject
	if attachment:
		#print("attaching:", attachment, file=sys.stderr)
		part=MIMEApplication(open(attachment, 'rb').read())
		part.add_header('Content-Disposition', 'attachment', filename=attachment)
		msg.attach(part)
	msg.preamble="Mulitpart message\n"
	s=smtplib.SMTP("smtp.gmail.com", 587)
	s.ehlo() #checks in with the server and verifies that we can proceed - I think this is some sort of security against spammers
	s.starttls()
	s.ehlo() #it needs to be run again after setting everything in encrypted mode with the starttls() command
	s.login(user, passwd)
	#print(msg.as_string(), file=sys.stderr)
	s.sendmail(msg['From'], msg['To'], msg.as_string())
	s.quit()


CHUNK = 2**11
RATE = 8000
CHANNELS = 1
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16, rate=RATE, channels=1, input=True, frames_per_buffer=CHUNK)

for i in range(int(time*(235))): #235 came from finding that there are 235 samples per minute, so 14100 samples per hour
	data = np.fromstring(stream.read(CHUNK,  exception_on_overflow = False ),dtype=np.int16)
	peak=np.average(np.abs(data))*2
	bars="#"*int(50*peak/2**16)
	print("%04d %05d %s"%(i,peak,bars), file=sys.stdout)
	if peak >threshhold: #only very loud barks
		if sendto:
			SendEmail(sendto, subject, body, attachment, args.fromEmail, args.passwd)
	if outfile:
		now = datetime.datetime.now()
		print(peak, now.strftime("%Y-%m-%d %H:%M"), file=OUT)
stream.stop_stream()
stream.close()
p.terminate()

#20:40.08
