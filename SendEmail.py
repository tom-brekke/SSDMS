#!/usr/bin/env python

#code to send an email
#from the rasPi ideas book
#modified by TDB on 31-01-2018

from __future__ import print_function
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import time
import argparse


parser=argparse.ArgumentParser()
parser.add_argument("--to", "-t", type=str, required=True, help="The recipient's email address")
parser.add_argument("--subject", "-s", type=str, required=True, help="The subject line of the email in quotes")
parser.add_argument("--fromEmail", "-t", type=str, required=True, help="The senders's email address")
parser.add_argument("--passwd", "-t", type=str, required=True, help="The sender's email password")
parser.add_argument("--body", "-b", type=str, required=False, default="", help="The body text of the email in quotes")
parser.add_argument("--attachment", "-a", type=str, required=False, default="", help="The name of the file to attach")

args=parser.parse_args()
sendto=args.to
subject=args.subject
body=args.body
attachment=args.attachment

def SendEmail(sendto, subject, body, attachment):
	user=args.fromEmail
	passwd=args.passwd
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
def main():
	SendEmail(sendto, subject, body, attachment)
	print("Email sent to", sendto, sep=" ", file=sys.stderr)
if __name__=="__main__":
	main()


