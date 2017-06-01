eventos <- read.csv("datos/focos_salida.csv")

eventos <- eventos[,c("incendio_id","incendio_tam","incendio_inicio","incendio_fin","incendio_centro_lat","incendio_centro_lon", "perimetro", "duracion", "velocidad")]

eventos <- eventos[-which(duplicated(eventos$incendio_id)),]


write.csv(x=eventos,file="datos/focos_salida_agrupados.csv",row.names = FALSE)
