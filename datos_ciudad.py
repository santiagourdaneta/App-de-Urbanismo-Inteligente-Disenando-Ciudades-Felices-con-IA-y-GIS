import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString # Asegúrate de importar LineString
import pandas as pd
import numpy as np
import os

def generar_datos_simulados_ciudad(num_edificios=50, num_parques=5, num_calles=10, area_ciudad=1000):
    """
    Simula datos de una ciudad: edificios, parques y calles.
    Los genera de forma aleatoria para que el robot tenga algo con lo que trabajar.
    """
    print("Generando bloques de ciudad (datos simulados)...")

    # Edificios (puntos y un pequeño polígono para su huella)
    edificios_data = []
    for i in range(num_edificios):
        x = np.random.uniform(0, area_ciudad)
        y = np.random.uniform(0, area_ciudad)
        punto_central = Point(x, y)
        huella = Polygon([(x-5, y-5), (x+5, y-5), (x+5, y+5), (x-5, y+5)])
        
        edificios_data.append({
            'id': i,
            'tipo': 'residencial' if np.random.rand() < 0.8 else 'comercial',
            'densidad_esperada': np.random.randint(10, 100),
            'antiguedad_anos': np.random.randint(1, 50),
            'geometry': punto_central,
            'huella_geom': huella
        })
    edificios_gdf = gpd.GeoDataFrame(edificios_data, geometry='geometry', crs="EPSG:4326")

    # Parques (polígonos)
    parques_data = []
    for i in range(num_parques):
        x_centro = np.random.uniform(0, area_ciudad)
        y_centro = np.random.uniform(0, area_ciudad)
        ancho = np.random.uniform(20, 100)
        alto = np.random.uniform(20, 100)
        parque_poly = Polygon([
            (x_centro - ancho/2, y_centro - alto/2),
            (x_centro + ancho/2, y_centro - alto/2),
            (x_centro + ancho/2, y_centro + alto/2),
            (x_centro - ancho/2, y_centro + alto/2)
        ])
        parques_data.append({
            'id': i,
            'nombre': f'Parque {i+1}',
            'area_m2': parque_poly.area,
            'geometry': parque_poly
        })
    parques_gdf = gpd.GeoDataFrame(parques_data, geometry='geometry', crs="EPSG:4326")

    # Calles (líneas)
    calles_data = []
    for i in range(num_calles):
        x1, y1 = np.random.uniform(0, area_ciudad), np.random.uniform(0, area_ciudad)
        x2, y2 = np.random.uniform(0, area_ciudad), np.random.uniform(0, area_ciudad)
        calle_line = LineString([(x1, y1), (x2, y2)])
        calles_data.append({
            'id': i,
            'nombre': f'Calle {i+1}',
            'longitud_m': calle_line.length,
            'tipo_trafico': np.random.choice(['alto', 'medio', 'bajo']),
            'geometry': calle_line
        })
    calles_gdf = gpd.GeoDataFrame(calles_data, geometry='geometry', crs="EPSG:4326")

    print(f"Generados {len(edificios_gdf)} edificios, {len(parques_gdf)} parques, {len(calles_gdf)} calles.")
    return edificios_gdf, parques_gdf, calles_gdf

def guardar_datos_ciudad(edificios_gdf, parques_gdf, calles_gdf):
    """Guarda los datos simulados en archivos geojson para que otros robots los lean."""
    print("Guardando bloques de ciudad...")
    edificios_gdf.to_file("data/edificios.geojson", driver="GeoJSON")
    parques_gdf.to_file("data/parques.geojson", driver="GeoJSON")
    calles_gdf.to_file("data/calles.geojson", driver="GeoJSON")
    print("Bloques de ciudad guardados en la carpeta 'data'.")

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
    
    edificios, parques, calles = generar_datos_simulados_ciudad()
    guardar_datos_ciudad(edificios, parques, calles)