---
title: Modelo de difusión de fuegos
author:
- Joaquin Torre Zaffaroni (joaquintorrezaffaroni@gmail.com)
toc: yes
---
## Introducción

El siguiente programa (o colección de *scripts*) es un modelo de agregación
que une varios focos de incendio en *eventos* de incendios. Se entiende que
un evento de incendio comprende varios focos, porque estos últimos son la
información más granular que da el satélite.   

## Instalación 

Estos scripts no se comportan como programas independientes (standalone), sino
que requieren un ambiente de desarrollo instalado. Para correr el código es
necesario tener los intérpretes y las librerías instaladas.

Para el flujo principal (detección de eventos de incendio, correlación con la
grilla y cálculo de estadísticas) sólo se requiere Python y sus librerías. Para
eso, la forma más sencilla es recurrir a un proyecto como
[WinPython](https://winpython.github.io/) o
[Anaconda](https://anaconda.org/anaconda/python). Lo requerido es que la versión
de Python a utilizar sea mayor a la 3.3.     

Es muy posible que el paquete `shapefile` no venga con estas suites, en ese caso
es necesario correr en una consola el siguiente comando:   
```
pip install pyshp
```

Para el análisis de la geometría de los eventos de incendio, es necesario tener
instalado R y el paquete 'ashape'. R se puede bajar desde la
[página](https://www.r-project.org/) del proyecto. Una vez instalado, en el
cliente se puede ejecutar el siguiente comando:   

```
install.packages('ashape')
```
y, luego de seleccionar los mirrors (conviene elegir el más cercano, como el de
la UNLP), el paquete se instala.

## Orden de scripts y flujos de los datos

Por convención, cada vez que se hace referencia a un archivo `csv` se asume que
se encuentra en la carpeta `datos`.    

1. `join_fires.py` toma una entrada (por defecto, `focos_recorte.csv`) y
detecta los eventos de incendio agrupando los focos. A las columnas de los focos
les agrega otras como a qué evento pertence, su tamaño, inicio, fin, etc. El
archivo de salida es `focos_salida.csv`.
2. (opcional) `eccentricity.R` analiza el archivo `focos_salida.csv` y genera
estadísticas para los eventos de incendios relacionados a su geometría. Deja
su salida en `focos_salida_eccentricity.R`.
2. `merge_incendios.py` agrupa las filas del archivo `focos_salida.csv`,
eliminando las columnas que están a nivel foco y dejando solo una fila para cada
evento de incendio. El archivo de salida es `focos_salida_agupados.csv`.
3. `procesar_incendios_grilla.py` toma un archivo de grilla (modificable
editando la variable `AR_GRILLA`), y a cada incendio le asigna una grilla. El
archivo de salida es `incendios_con_celdas.csv`.
4. `fire_phenology.py` genera estadísticas sobre los eventos de incendio en
cada celda por cada año o por cada mes. Los archivos de salida son
`estadisticas_anuales.csv` y `estadisticas_mensuales.csv`.    

## Uso de los scripts en Python    

### Desde la consola   
Por ejemplo desde linux, basta utilizar lo siguiente:
```
$ python3 join_fires.py
```
asumiendo que ya se está en el directorio que contiene ese script. El cliente de
Python puede ser `python3`, pero depende del método de instalación. Generalmente
`python` es Python 2.x, por lo que no nos sirve.
El primer script, `join_fires.py` puede requerir un poco de configuración en la
primera corrida: para definir el archivo de entrada, el separador del csv, el
punto decimal que se utiliza y el formato de la fecha. Estos valores se pueden
modificar observando las primeras líneas del archivo, editables con cualquier
editor de texto plano (Spyder, Notepad++, SublimeText, Atom, Notepad...).
Los demás scripts no requieren eso, ya que trabajan sobre la representación
interna de los datos, invariante a la entrada.   

### Desde un IDE   
Para esto, simplemente es necesario abrir el script que se quiere ejecutar y
correrlo según especifica el IDE. En muchos, la tecla F5 se encarga de esto. Se
aplica la misma nota sobre el primer script de `join_fires.py` 
que está escrita en el apartado anterior.
### Desde la interfaz     
Hay una interfaz en desarrollo que haría un poco más sencillo manejar el flujo.
Todavía tiene algunos problemas, pero también es útil. Visualmente, además
muestra una barra de progreso. Se puede ejecutar corriendo el archivo `gui.py`.

## Uso de los scripts en R    

Se puede abrir el IDE que esté instalado para R (cuando se instala R viene uno
por defecto, pero también hay uno muy bueno que se llama RStudio), abrir el
script a ejecutar y ejecutarlo según el IDE (cliqueando en 'Source', apretando
en F5, etc.).   
