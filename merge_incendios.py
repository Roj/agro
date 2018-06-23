import pandas as pd

DEFAULT_FILENAME_IN = "datos/focos_salida.csv"
DEFAULT_FILENAME_OUT = "datos/focos_salida_agrupados.csv" 
def merge_incendios(filename_in = DEFAULT_FILENAME_IN, filename_out =
DEFAULT_FILENAME_OUT):
    focos_salida = pd.read_csv(filename_in)

    del focos_salida['object_id']
    del focos_salida['latitude']
    del focos_salida['longitude']
    del focos_salida['fecha']

    focos_salida.drop_duplicates("incendio_id","first").to_csv(filename_out, 
        index=False)
    del focos_salida

if __name__ == "__main__":
    merge_incendios()
