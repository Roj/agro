library("aspace")

datos <- read.csv("datos/focos_salida.csv")

datos$Sigma.x <- -1
datos$Sigma.y <- -1
datos$Excentricidad <- -1
datos$Theta <- -1
#wrap this around every incendio_id
for (i in seq(0, max(datos$incendio_id))) {
  rows <- datos$incendio_id == i

  if (sum(rows) < 3)
      next
  
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
    datos$Excentricidad[rows] <- r.SDE$Eccentricity
  } else {
    print(paste("Fails for i = ", i))
  }
}
#failing <- c(1996, 7407, 15798)