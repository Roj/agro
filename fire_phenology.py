import pandas as pd
AR_IN = "datos/incendios_con_celdas.csv"
AR_OUT_ANUAL = "datos/estadisticas_anuales.csv"
AR_OUT_MENSUAL = "datos/estadisticas_mensuales.csv"

def analizar_fenologia():
    datos = pd.read_csv(AR_IN)
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
    del promedios['bright']
    del promedios['bright_mean']
    del promedios['bright_sd']
    del promedios['frp']
    del promedios['frp_mean']
    del promedios['frp_sd']
    del promedios['conf']
    del promedios['conf_mean']
    del promedios['conf_sd']
    promedios.columns = ['duracion_prom','incendio_tam_prom', 'perimetro_prom', 'velocidad_prom']

    resultado = promedios
    resultado['num_eventos'] = agrupados['incendio_tam'].sum()
    resultado = resultado.reset_index()
    anuales = resultado.groupby(["celda","year"], as_index=False)
    def func(group): return group.loc[group['num_eventos'] == group['num_eventos'].max()]

    anuales = anuales.apply(func).reset_index()

    anuales.to_csv(AR_OUT_ANUAL)
    resultado.to_csv(AR_OUT_MENSUAL)
    del anuales
    del resultado
    del promedios
    del datos

if __name__ == "__main__":
    analizar_fenologia()
