setwd("/home/joaquintz/Desktop/research/agro/datos")
library("ggplot2")
options(stringsAsFactors = FALSE)

focos <- read.csv("focos_recorte.csv")
head(focos$ACQ_DATE)
head()

head(focos)
focos$ACQ_DATE <- as.Date(focos$ACQ_DATE,format="%m/%d/%Y")

p<-ggplot(data=focos,aes(x=ACQ_DATE,y=BRIGHTNESS,colour=SATELLITE))+geom_point()
print(p)

library("PerformanceAnalytics")
focos.numericos <- data.frame(
  focos$LATITUDE,
  focos$LONGITUDE,
  focos$BRIGHTNESS,
  focos$SCAN,
  focos$TRACK,
#  focos$ACQ_DATE,
  focos$ACQ_TIME)
chart.Correlation(focos.numericos)