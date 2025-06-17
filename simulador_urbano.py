import geopandas as gpd
from shapely.geometry import Point, Polygon
import pandas as pd
import numpy as np
import joblib
import os

# Cargar los modelos entrenados
modelo_felicidad = None
modelo_trafico = None
modelo_salud_mental = None

def cargar_todos_los_modelos():
    global modelo_felicidad, modelo_trafico, modelo_salud_mental
    print("Cargando todos los cerebritos adivinadores...")
    try:
        modelo_felicidad = joblib.load('modelos/modelo_felicidad.pkl')
        modelo_trafico = joblib.load('modelos/modelo_trafico.pkl')
        modelo_salud_mental = joblib.load('modelos/modelo_salud_mental.pkl')
        print("Cerebritos cargados.")
        return True
    except FileNotFoundError:
        print("Error: Uno o más modelos no se encontraron. Asegúrate de ejecutar 'modelo_impacto.py' primero.")
        return False

def simular_nuevo_desarrollo(
    nombre_proyecto,
    tipo_desarrollo, # 'residencial', 'comercial', 'mixto'
    latitud, longitud, 
    densidad_poblacional_estimada, # Personas por hectárea o por edificio
    area_m2,
    cercania_a_parques_m=None,
    cercania_a_escuelas_m=None,
    presencia_comercio_local_bool=None
):
    """
    Simula el impacto de un nuevo desarrollo urbano.
    Recibe la información del nuevo proyecto y usa los modelos para predecir.
    """
    if not (modelo_felicidad and modelo_trafico and modelo_salud_mental):
        print("¡Los cerebritos no están cargados! No puedo adivinar.")
        return

    print(f"\nSimulando nuevo desarrollo: '{nombre_proyecto}' ({tipo_desarrollo})")
    
    # Preparar las características para la predicción
    if cercania_a_parques_m is None:
        cercania_a_parques_m = np.random.uniform(0.1, 10.0)
    if cercania_a_escuelas_m is None:
        cercania_a_escuelas_m = np.random.uniform(0.01, 5.0)
    if presencia_comercio_local_bool is None:
        presencia_comercio_local_bool = np.random.randint(0, 2)

    tipo_indexed = 0 if tipo_desarrollo == 'residencial' else (1 if tipo_desarrollo == 'comercial' else 0.5)

    # Crear un DataFrame de Pandas para la predicción
    # Las columnas deben coincidir EXACTAMENTE con las features usadas en modelo_impacto.py
    datos_para_predecir = pd.DataFrame([{
        'distancia_a_parque': cercania_a_parques_m,
        'densidad_esperada': densidad_poblacional_estimada,
        'antiguedad_anos': 1, # Asumimos que es nuevo, 1 año
        'tipo_indexed': tipo_indexed,
        'cercania_a_escuelas': cercania_a_escuelas_m,
        'presencia_comercio_local': presencia_comercio_local_bool
    }])

    # Realizar Predicciones
    # Asegúrate de usar los nombres de las características que el modelo espera
    felicidad_predicha = modelo_felicidad.predict(datos_para_predecir[modelo_felicidad.feature_names_in_])[0]
    trafico_predicho = modelo_trafico.predict(datos_para_predecir[modelo_trafico.feature_names_in_])[0] # Devuelve 0 o 1
    salud_mental_predicha = modelo_salud_mental.predict(datos_para_predecir[modelo_salud_mental.feature_names_in_])[0]

    # Diagnóstico y sugerencias
    problemas_potenciales = []
    sugerencias = []

    if felicidad_predicha < 5:
        problemas_potenciales.append("Bajo nivel de felicidad proyectado.")
        sugerencias.append("Considerar más áreas verdes o espacios comunitarios.")
    
    if trafico_predicho == 1:
        problemas_potenciales.append("Alto impacto en el tráfico esperado.")
        sugerencias.append("Planificar infraestructura de transporte público o calles más amplias.")

    if salud_mental_predicha < 5:
        problemas_potenciales.append("Posible impacto negativo en la salud mental de residentes.")
        sugerencias.append("Integrar diseño biofílico y espacios de calma.")

    print("\n--- Resultados de la Simulación ---")
    print(f"Puntuación de Felicidad Predicha (0-10): {felicidad_predicha:.2f}")
    print(f"Impacto en el Tráfico Predicho (0=Bajo, 1=Alto): {'Alto' if trafico_predicho == 1 else 'Bajo'}") # Traducir 0/1 a texto
    print(f"Puntuación de Salud Mental Predicha (0-10): {salud_mental_predicha:.2f}")

    if problemas_potenciales:
        print("\n¡Problemas Potenciales Detectados ANTES de Construir!:")
        for p in problemas_potenciales:
            print(f"- {p}")
        print("\nSugerencias para un Urbanismo Más Inteligente:")
        for s in sugerencias:
            print(f"- {s}")
    else:
        print("\n¡Excelente! No se detectaron problemas mayores con esta propuesta.")

if __name__ == "__main__":
    if cargar_todos_los_modelos():
        simular_nuevo_desarrollo(
            nombre_proyecto="Nuevo Edificio Residencial 'Sol Naciente'",
            tipo_desarrollo="residencial",
            latitud=-12.046374,
            longitud=-77.042793,
            densidad_poblacional_estimada=70,
            area_m2=1500,
            cercania_a_parques_m=0.5,
            cercania_a_escuelas_m=0.8,
            presencia_comercio_local_bool=1
        )

        simular_nuevo_desarrollo(
            nombre_proyecto="Gran Centro Comercial 'La Palmera'",
            tipo_desarrollo="comercial",
            latitud=-12.050000,
            longitud=-77.060000,
            densidad_poblacional_estimada=200,
            area_m2=10000,
            cercania_a_parques_m=5.0,
            cercania_a_escuelas_m=3.0,
            presencia_comercio_local_bool=0
        )
    else:
        print("No se pueden ejecutar simulaciones sin los modelos entrenados.")