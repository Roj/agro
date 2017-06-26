#!/usr/bin/python
from __future__ import division
import datetime
import csv
from scipy.spatial import ConvexHull
from scipy.spatial.qhull import QhullError
import numpy as np
from math import asin,sqrt,sin,cos,pi
from UnionFind import UnionFind
import sys, os

#hay varios de la misma? => parece ser que no

ARCHIVO_FOCOS = "datos/focos-pro.csv"
ARCHIVO_SALIDA= "datos/focos_salida.csv"
#excel: separador es ; punto decimal es ,
#mundo racional: separador es , punto decimal es .
SEPARADOR=";"
PUNTO_DECIMAL=","
#"%m/%d/%Y" focos_recorte.csv
#excel => "%d/%m/%Y" 
FORMATO_FECHA = "%d/%m/%Y" 
CORTE_DIST_HAVERSINE=2

#grados a radianes
def d2r(x):	return pi*x/180

#geodesica de haversine
def haversine(lat1,lon1,lat2,lon2):
	lon1, lat1 = d2r(lon1), d2r(lat1)
	lon2, lat2 = d2r(lon2), d2r(lat2)

	return (
		2*6372.8
		* asin(sqrt(
			sin((lat2-lat1)/2)**2
			+ ( cos(lat1)
				* cos(lat2)
				* sin((lon2-lon1)/2)**2)
		))
	)
#incendio es un grupo de focos,
#pero la referencia es en sentido foco->incendio
#i.e., cada foco sabe a que incendio pertenece.
#el incendio tiene estadisticas sobre si mismo, that's all
class Incendio:
	def __init__(self,g_id,fecha,poss):
		self.id = g_id
		self.tam = 1
		self.inicio = fecha
		self.fin = fecha
		self.posiciones = poss
		self._cache_perimetro = None
		self._cache_perim_n = None
		self.lista_latlon=list()
		self.prom_lat = -1
		self.prom_lon = -1
	#wrapper para haversine, pero en otro formato
	def _dist(self, origen, destino):
		#punto[lon,lat] -> haversine(lat,lon)
		return haversine(origen[1],origen[0],destino[1],destino[0])

	def _calcular_perimetro(self):
		#calcula el perimetro a traves del casco convexo de los puntos.
		#actualmente perimetro = sum(dist(centroides)), no tiene en cuenta los bordes de las celdas.
		#tiene un cache just in case para no calcularlo dos veces.
		if (self._cache_perimetro is not None) and (self._cache_perim_n == len(self.posiciones)):
			#si, falla cuando calculas perimetro, borras y agregas un elemento distinto, calc. de nuevo
			#en este flujo no sucede // si se cambia, hay que agregar una revision distinta (e.g. md5)
			return self._cache_perimetro

		perimetro = 0
		puntos = np.array(self.posiciones)

		#caso trivial: no hay suficientes puntos
		if len(self.posiciones) < 3:
			for i in range(1,puntos.shape[0]):
				perimetro += self._dist(puntos[i],puntos[i-1])
			self._cache_perimetro = perimetro
			self._cache_perim_n = len(self.posiciones)
			return perimetro
		#QJ=si son coplanares, este parametro los mueve un cachito para que los encuentre
		#Pp=no imprimir errores de precision
		hull = ConvexHull(puntos, qhull_options='QJ Pp')
		#los vertices estan ordenados ya
		for i in range(1, hull.vertices.shape[0]):
			perimetro+= self._dist(puntos[hull.vertices[i]],puntos[hull.vertices[i-1]])
		#wrap-around
		perimetro+=self._dist(
			puntos[hull.vertices[hull.vertices.shape[0]-1]],
			puntos[hull.vertices[0]]
		)
		self._cache_perimetro = perimetro
		self._cache_perim_n = len(self.posiciones)
		return perimetro


	def promediar_latlons(self):
		if self.prom_lat == -1 and self.prom_lon == -1:
			lats, lons = zip(*self.lista_latlon)
			self.prom_lat = sum(lats)/len(lats)
			self.prom_lon = sum(lons)/len(lons)
		
	def lista_nombres(self):
		return [
			"incendio_id",
			"incendio_tam",
			"incendio_inicio",
			"incendio_fin",
			"incendio_centro_lat",
			"incendio_centro_lon",
			"perimetro",
			"duracion",
			"velocidad"
		]
	def lista(self):
		self.promediar_latlons()
		days = (self.fin-self.inicio).days+1
		return [
			self.id,
			self.tam,
			self.inicio,
			self.fin,
			self.prom_lat,
			self.prom_lon,
			self._calcular_perimetro(),
			days,
			self.tam/days
		]
class Foco:
	_uniqid = 0
	def __init__(self,f_id,lat,lon,fecha):
		self.id = Foco._uniqid
		Foco._uniqid+=1
		self.objectid = f_id
		self.lat = lat
		self.lon = lon
		self.fecha = fecha
		self.grupo = Incendio(self.id,self.fecha, [self.obtener_pos()])
	def obtener_pos(self):
		return [self.lon, self.lat]
	def es_ady(self,otro,corte=CORTE_DIST_HAVERSINE):
		return haversine(
			self.lat,self.lon,
			otro.lat,otro.lon
		) < corte
	def lista_nombres(self):
		nombres = [
			"object_id",
			"latitude",
			"longitude",
			"fecha"
		]
		return nombres + self.grupo.lista_nombres()
	def lista(self):
		props = [
			self.objectid,
			self.lat,
			self.lon,
			self.fecha
		]
		return props + self.grupo.lista()
	

def crear_foco(diccionario):
    
	return Foco(
		int(diccionario["OBJECTID"]),
		float(diccionario["LATITUDE"].replace(PUNTO_DECIMAL,".")),
		float(diccionario["LONGITUDE"].replace(PUNTO_DECIMAL,".")),
		datetime.datetime.strptime(diccionario["ACQ_DATE"],FORMATO_FECHA)
	)

class Difusion:
	def __init__(self):
		self.focos = None
		#Union-find/DisjSet de fuegos
		self.uf_fuegos = None
		#Lista de dias con listas de incendios
		self.dias = dict()
	def cargar_de_archivo(self,ARCHIVO_FOCOS):
		with open(ARCHIVO_FOCOS,"r") as f:
			reader = csv.DictReader(f,delimiter=SEPARADOR)
			ar_focos = list(reader)
		self.focos = list(map(crear_foco,ar_focos))
	def cargar(self,focos):
		self.focos = focos
	def _cargar_estructuras(self):
		self.uf_fuegos = UnionFind(len(self.focos))
		for foco in self.focos:
			if foco.fecha not in self.dias:
				self.dias[foco.fecha]=list()
			#agrupo por dias
			self.dias[foco.fecha].append(foco)

		self.dias = self.dias.values()
		self.dias = sorted(self.dias,key = lambda dia: dia[0].fecha)
	def union_fire(self,focos_ayer,focos_hoy):
		for foco_hoy in focos_hoy:
			for foco_ayer in focos_ayer:
				if foco_hoy.es_ady(foco_ayer):
					self.uf_fuegos.union(foco_hoy.id,foco_ayer.id)

		#ahora apareo los del mismo dia; pero optimizando el ciclo
		#(la optimizacion clasica de bubble sort)
		for i in range(len(focos_hoy)):
			for j in range(i,len(focos_hoy)):
				if focos_hoy[i].es_ady(focos_hoy[j]):
					self.uf_fuegos.union(focos_hoy[i].id,focos_hoy[j].id)
	def calc_estadisticas(self):
		for foco in self.focos:
			if foco.id != foco.grupo.id:
				foco.grupo.tam+=1
				foco.grupo.posiciones.append(foco.obtener_pos())
			foco.grupo.lista_latlon.append((foco.lat,foco.lon))
			if foco.grupo.fin<foco.fecha:
				foco.grupo.fin=foco.fecha

	def correr(self):
		if len(self.dias) == 0: self._cargar_estructuras()
		i=1
		n=len(self.dias)
		prev=self.dias[0]
		#la lista esta implementada internamente como un vector, por lo que el
		#acceso al i-esimo elemento es O(1)
		while i<n:
			self.union_fire(prev,self.dias[i])
			prev = self.dias[i]
			i+=1	
		#ahora le asigno a cada foco su incendio
		for foco in self.focos:
			foco.grupo=self.focos[self.uf_fuegos[foco.id]].grupo

		self.calc_estadisticas()
	def guardar_en_archivo(self, ARCHIVO_SALIDA):
		with open(ARCHIVO_SALIDA,"w") as f:
			writer = csv.writer(f)
			writer.writerow(self.focos[0].lista_nombres())
			for foco in self.focos:
				writer.writerow(foco.lista())

		
if __name__ == "__main__":
	app = Difusion()
	app.cargar_de_archivo(ARCHIVO_FOCOS)
	app.correr()
	app.guardar_en_archivo(ARCHIVO_SALIDA)
