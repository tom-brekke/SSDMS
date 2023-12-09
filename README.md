# SSDMS
#Sausage Dog Monitoring System

#This is a bit of code that is to be run on a raspberryPI connected to an old webcam. 

#it monitors the decibels of noise in the house and when the volume reaches a critical threshold, takes a picture, attaches the picture to an email and sends the email to a specified recipient. It also writes the decibels out to a flat text file that can be plotted.

#we used it to monitor our sausage dog at home when we were at work and from the data generated were able to figure out when the postman came to the door each day.


# it was written in 2017/2018 and used a now-deprecated way to use gmail to send emails out. 

#as a bit of a laugh, we also tied it into twitter and made the dogs an account. Every time they barked at home they also sent out a tweet saying "bark" or "barkbark" or some such variation. The plan was originally a deadban "bark" everytime, but at the time twitter didn't allow two of the exact same tweets to be sent out, so I had it draw from a random set each time.  
