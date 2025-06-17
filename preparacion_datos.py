import geopandas as gpd
import pandas as pd
import numpy as np
import os

def cargar_y_limpiar_datos_espaciales():
    """
    Carga los datos de los bloques de ciudad y los limpia un poco.
    Usamos Pandas y GeoPandas para esto.
    """
    print("Cargando y limpiando bloques de ciudad con Pandas y GeoPandas...")

    try:
        edificios_gdf = gpd.read_file("data/edificios.geojson")
        parques_gdf = gpd.read_file("data/parques.geojson")
        calles_gdf = gpd.read_file("data/calles.geojson")
    except Exception as e:
        print(f"Error al cargar archivos GeoJSON: {e}. Asegúrate de que los archivos existan en la carpeta 'data'.")
        return None, None, None

    # Añadir columna de "distancia a parque" (simulada)
    # En un análisis real, calcularías la distancia al parque más cercano usando las geometrías.
    edificios_gdf['distancia_a_parque'] = np.random.uniform(0.1, 10.0, len(edificios_gdf))
    
    # Añadir columna de "nivel de ruido" (simulada, basada en tipo de tráfico)
    # Primero, unimos algunas características de las calles a los edificios para simular impacto
    # Esto es una simplificación grande; en lo real, se harían análisis de proximidad y densidad.
    edificios_gdf['nivel_ruido_promedio'] = np.random.choice([30.0, 50.0, 80.0], len(edificios_gdf)) # Simulamos el ruido

    # Convertir tipo de edificio a números para la IA (One-Hot Encoding con Pandas)
    edificios_gdf = pd.get_dummies(edificios_gdf, columns=['tipo'], prefix='tipo')
    # Nos aseguramos de tener 'tipo_residencial' y 'tipo_comercial'
    if 'tipo_residencial' not in edificios_gdf.columns:
        edificios_gdf['tipo_residencial'] = 0
    if 'tipo_comercial' not in edificios_gdf.columns:
        edificios_gdf['tipo_comercial'] = 0
    
    print("Bloques de ciudad cargados y pre-procesados.")
    return edificios_gdf, parques_gdf, calles_gdf

if __name__ == "__main__":
    if not os.path.exists('data'):
        print("La carpeta 'data' no existe. Ejecuta 'python datos_ciudad.py' primero.")
    else:
        if not os.path.exists('data/edificios.geojson'):
             print("Archivos GeoJSON no encontrados en 'data'. Ejecuta 'python datos_ciudad.py' primero.")
        else:
            edificios_df, parques_df, calles_df = cargar_y_limpiar_datos_espaciales()
            
            if edificios_df is not None and parques_df is not None and calles_df is not None:
                print("\nPrimeras filas de edificios procesados:")
                print(edificios_df.head())
                print("\nColumnas de edificios procesados:")
                print(edificios_df.columns)