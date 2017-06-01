# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 12:57:59 2017

@author: joaquintz
"""

import shapefile
import csv
AR_GRILLA = "DATOS-PRUEBA_RECORTE/GRILLA"
AR_CSV = "datos/focos_salida_agrupados.csv"
AR_CSV_OUT = "datos/incendios_con_celdas.csv"

#ordena los puntos para estar seguro de cual es cual
#devuelve #[(izq,inf),(izq,sup),(der,inf),(der,sup)]
def ordenar_vertices(puntos):
	#primero elimino duplicados que hay because reasons
	puntos = list(set(puntos))
	
	#ordeno por Y ascendente
	puntos.sort(key=lambda punto: punto[1])
	#ordeno por X ascendente, como el sort es estable, se mantiene el ord ant.
	puntos.sort(key=lambda punto: punto[0])
	#el orden ahora es:
	#[izq_inf,izq_sup,der_inf,der_sup]
	return puntos


def pertenece(punto,cuadrado):
	x_izq, y_inf = cuadrado[0]
	x_der, y_sup = cuadrado[3]
	x,y = punto
	return (x_izq <= x <= x_der) and (y_inf <= y <= y_sup)

def celda_pert(punto, cuadrados):
	i=0
	n = len(cuadrados)
	while (i<n) and (not pertenece(punto, cuadrados[i])):
		i+=1
	
	if i==n: return -1 #no se encontro cuadrado
	return i

grilla = shapefile.Reader(AR_GRILLA)
cuadrados = [ordenar_vertices(s.points) for s in grilla.shapes()]


if __name__ == "__main__":

	with open(AR_CSV,"r") as f:
		reader = csv.DictReader(f)
		incendios = list(reader)

	for incendio in incendios:
		incendio["celda"]=celda_pert(
			(float(incendio["incendio_centro_lon"]),float(incendio["incendio_centro_lat"])),
			cuadrados
		)
	print("got here!")
	with open (AR_CSV_OUT, "w") as f:
		writer = csv.DictWriter(f,fieldnames=sorted(incendios[0].keys()))
		writer.writeheader()
		writer.writerows(incendios)

	
