import pandas as pd

focos_salida = pd.read_csv("datos/focos_salida.csv")

del focos_salida['object_id']
del focos_salida['latitude']
del focos_salida['longitude']
del focos_salida['fecha']

focos_salida.drop_duplicates("incendio_id","first").to_csv("datos/focos_salida_agrupados.csv")
