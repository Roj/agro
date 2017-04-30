setwd("/home/joaquintz/research/agro/datos")
library("ggplot2")
library("ggmap")
options(stringsAsFactors = FALSE)

focos <- read.csv("focos_recorte.csv")
focos$ACQ_DATE <- as.Date(focos$ACQ_DATE,format="%m/%d/%Y")
focos.red <- focos[,c(1,2,3,7)]
p<-ggplot(data=focos,aes(x=ACQ_DATE,y=BRIGHTNESS,colour=SATELLITE))+geom_point()
print(p)

library("PerformanceAnalytics")
focos.numericos <- data.frame(
  focos$BRIGHTNESS,
  focos$SCAN,
  focos$TRACK,
#  focos$ACQ_DATE,
  focos$ACQ_TIME,
  focos$BRIGHT_T31,
  focos$FRP)
chart.Correlation(focos.numericos)

latlons <- data.frame(focos$LONGITUDE,focos$LATITUDE)
latlons <- latlons[-duplicated(latlons),]
names(latlons)<-c("lon","lat")

#mapa sobre celdas
mapa_base <- ggmap(
  get_map(location=c(lon=mean(latlons$lon),lat=mean(latlons$lat)),zoom=8)
)
mapita <- mapa_base+geom_point(aes(x=lon,y=lat),data=latlons)
print(mapita+ggtitle("Celdas de satelite en la muestra"))

#mapa de cant eventos
mapita <- mapa_base+stat_density2d(aes(x=LONGITUDE,y=LATITUDE),data=focos)
print(mapita+ggtitle("Heatmap de eventos"))

#mapa de brightness
mapita <- mapa_base+geom_point(aes(x=LONGITUDE,y=LATITUDE,colour=BRIGHTNESS),size=0.4,alpha=0.3,data=focos)
mapita <- mapita + scale_colour_gradient(low="green",high="red")
print(mapita+ggtitle("Brillo de los eventos"))

names(focos) <- c(
  "oID","Latitude","Longitude","Brightness",
  "Scan","Track","ACQ_DATE","ACQ_TIME","Satellite",
  "Instrument","Confidence","Version","BRIGHT_T31",
  "FRP"
)
incendios_en_intervalo <- function(ini,fin) {
  ini.d <- as.Date(ini)
  fin.d <- as.Date(fin)
  focos.intervalo <- focos[which(ini.d<=focos$ACQ_DATE & focos$ACQ_DATE<=fin.d),]
  mapita <- mapa_base+geom_point(aes(x=Longitude,y=Latitude,colour=Brightness),size=0.4,alpha=0.3,data=focos.intervalo)
  mapita <- mapita + scale_colour_gradient(low="green",high="red",limits=c(200,510))
  print(mapita+ggtitle(paste("Brillo de los eventos entre ",ini,"y",fin,sep=" ")))
}
#incendios_en_intervalo(as.Date("2016-01-01"),as.Date("2017-01-01"))

for(month in seq(12*16)) {
  ini<-paste(2001+month%/%12,"-",month%%12+1,"-01",sep="")
  fin<-paste(2001+(month+1)%/%12,"-",(month+1)%%12+1,"-01",sep="")
  incendios_en_intervalo(ini,fin)
  ggsave(paste("incendio_",month,".png",sep=""))
}