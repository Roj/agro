library("aspace")

datos <- read.csv("datos/focos_salida.csv")

datos$Sigma.x <- -1
datos$Sigma.y <- -1
datos$Eccentricity <- -1
datos$Theta <- -1
errores_pf <- 0
#wrap this around every incendio_id
for (i in seq(0, max(datos$incendio_id))) {
  rows <- datos$incendio_id == i

  if (sum(rows) < 3)
      next
  #En esta variable global la función impura calc_sde almacena su resultado.
  r.SDE <- NULL
  #Por razones ilógicas, calc_sde hace print() de muchos valores. Correr esta
  #funcion sobre datos grandes llenaria el buffer de stdout y haría más lento
  #todo. Entonces, tenemos que suprimir esos valores.
  try(invisible(capture.output(attributes <- calc_sde(
    id = 1, filename = "SDE_Output.txt", centre.xy = NULL, calccentre = TRUE, 
    weighted = FALSE, weights = NULL, points = datos[rows, c("latitude", "longitude")],
    verbose = FALSE))))
  if (! is.null(r.SDE)) {
    datos$Sigma.x[rows] <- r.SDE$Sigma.x
    datos$Sigma.y[rows] <- r.SDE$Sigma.y
    datos$Theta[rows] <- r.SDE$Theta
    datos$Eccentricity[rows] <- r.SDE$Eccentricity
  } else {
    #En la libreria 'aspace' hay un error de punto flotante: en una raiz cuadrada
    #no se revisa que el numero puede ser cero negativo (i.e. 0 - epsilon)
    #y en esos casos falla.
    print(paste("Error de punto flotante en el evento i = ", i))
    errores_pf <- errores_pf + 1
  }
}
print(paste("En total hubo ", errores_pf, "/", nrow(datos), " = ", 
            errores_pf/nrow(datos)*100, "% errores de punto flotante"))
datos <- datos[which(datos$Sigma.x != -1),]
print("Guardando datos en datos/focos_salida_eccentricity.csv")
write.csv(datos, "datos/focos_salida_eccentricity.csv", row.names = F)