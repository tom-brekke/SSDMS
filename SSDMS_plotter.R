#!/usr/bin/env Rscript

format_data<-function(SSDMS_df){
	colnames(SSDMS_df)<-c("vol", "V2", "V3")
	SSDMS_df$datetime<-as.POSIXct(paste(SSDMS_df$V2, SSDMS_df$V3), format="%Y-%m-%d %H:%M:%OS")
	SSDMS_df$time<-as.POSIXct(paste(SSDMS_df$V3), format="%H:%M:%OS")
	SSDMS_df$weekday<-as.POSIXlt(SSDMS_df$datetime)$wday
	return(SSDMS_df)
}

setwd("~/Documents/Raspberry_Pi_projects/SSDMS/")
files<-list.files(pattern="*.txt");files
alldata<-NULL
for(file in files){
	cat("Reading in File:", file, "\n")
	tmp<-format_data(read.table(file))
	alldata<-rbind.data.frame(alldata, tmp)
}

#plot everything by date:
#plot(y=alldata$vol, x=alldata$datetime, cex=.1, type="l", xlab="Time", ylab="Volume", bty="L")

#plot it all by time (kinda messy - not great):
#plot(y=alldata$vol, x=alldata$time, pch=19, cex=.1, type="p", col=alldata$weekday) 


#breaks for the below histograms
#c(0:144)*60*60/6 #for every 10 minutes
#c(0:96)*60*60/4  #for every 15 minutes
#c(0:48)*60*60/2  #for every 30 minutes
#c(0:24)*60*60    #for every 60 minutes
threshhold=15000
breaks=c(0:144)*60*60/6 
origin=as.Date(as.POSIXlt(Sys.time()))
weekdays=c("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
colors=c("#ffffb2", "#fed967", "#feb24c", "#fd8d3c", "#fc4e2a", "#e31a1c", "#b10026")
pdf("~/Documents/Raspberry_Pi_projects/SSDMS/Barks_by_day_of_week.pdf", width=7, height=21)
par(mfrow=c(11,1))
cat ("Plotting total density distribution for all days\n")
hist(alldata$time[alldata$vol>threshhold], breaks=as.POSIXct(breaks, origin=origin), freq=F, col="blue", axes=F, main="All days", xlab="time of day", plot=T);axis(2);axis.POSIXct(side=1, x=as.POSIXct(paste(alldata$time), format="%H:%M:%OS"));lines(density(as.numeric(as.POSIXct(alldata$time[alldata$vol>threshhold]))), col="blue", lwd=2); 


cat ("Plotting bark frequency for weekdays\n")
#hist for weekends
hist(alldata$time[alldata$vol>threshhold & alldata$weekday%in%c(1:5)], breaks=as.POSIXct(breaks, origin=origin), freq=T, col="darkblue", axes=F, main="Bark frequency for Weekdays", xlab="time of day", ylim=c());axis(2);axis.POSIXct(side=1, x=as.POSIXct(paste(alldata$time), format="%H:%M:%OS"))

cat ("Plotting bark frequency for weekends\n")
#hist for weekdays
hist(alldata$time[alldata$vol>threshhold & alldata$weekday%in%c(0,6)], breaks=as.POSIXct(breaks, origin=origin), freq=T, col="lightblue", axes=F, main="Bark frequency on Weekends", xlab="time of day");axis(2);axis.POSIXct(side=1, x=as.POSIXct(paste(alldata$time), format="%H:%M:%OS"))


cat("Density distribution of barks on weekdays vs weekends\n")
plot(density(as.numeric(as.POSIXct(alldata$time[alldata$vol>threshhold & alldata$weekday%in%c(1:5)]))), col="darkblue", lwd=2, axes=F, main="Density distribution of barks:\n weekends vs weekdays", xlim=as.POSIXct(c("00:00", "24:00"), format="%H:%M"), xlab="time of day"); axis(2);axis.POSIXct(side=1, x=as.POSIXct(paste(alldata$time), format="%H:%M:%OS"));
#here is the line for weekends
lines(density(as.numeric(as.POSIXct(alldata$time[alldata$vol>threshhold & alldata$weekday%in%c(0,6)]))), col="lightblue", lwd=2); 
legend(x=as.POSIXct("00:30", format="%H:%M"), y=4.5e-5, legend=c("Weekdays", "Weekends"), fill=c("darkblue", "lightblue"))




for (i in 0:6){
	cat("Histogram of Barks for", weekdays[i+1], "\n")
	hist(alldata$time[alldata$vol>threshhold & alldata$weekday==i], breaks=as.POSIXct(breaks, origin=origin), freq=T, col=colors[i+1], axes=F, main=paste("Frequency of barks on", weekdays[i+1]), xlab="time of day");
	axis(2);
	axis.POSIXct(side=1, x=as.POSIXct(paste(alldata$time), format="%H:%M:%OS"))
}
dev.off()

cat("finished plotting barks")
