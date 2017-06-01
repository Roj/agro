import pandas as pd
pd.read_csv("datos/incendios_con_celdas.csv")
datos = pd.read_csv("datos/incendios_con_celdas.csv")
datos['incendio_inicio'] = pd.to_datetime(datos['incendio_inicio'])
datos['incendio_fin'] = pd.to_datetime(datos['incendio_fin'])
datos['mes']=datos['incendio_inicio'].map(lambda fecha: fecha.month)
datos['year']=datos['incendio_inicio'].map(lambda fecha: fecha.year)
agrupados = datos.groupby(['celda','mes','year'])
promedios = agrupados.mean()
promedios.head()

del promedios['incendio_centro_lat']
del promedios['incendio_centro_lon']
del promedios['incendio_id']
promedios.columns = ['duracion_prom','incendio_tam_prom', 'perimetro_prom', 'velocidad_prom']

resultado = promedios
resultado['num_eventos'] = agrupados['incendio_tam'].sum()
resultado = resultado.reset_index()
anuales = resultado.groupby(["celda","year"], as_index=False)
def func(group): return group.loc[group['num_eventos'] == group['num_eventos'].max()]

anuales = anuales.apply(func).reset_index()

anuales.to_csv("datos/estadisticas_anuales.csv")
resultado.to_csv("datos/estadisticas_mensuales.csv")
