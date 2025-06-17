import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor # Para felicidad y salud mental (regresión)
from sklearn.linear_model import LogisticRegression # Para tráfico (clasificación)
from sklearn.metrics import mean_absolute_error, accuracy_score
import joblib # Para guardar y cargar modelos
import os

# --- Simulación de carga de datos para el entrenamiento ---
def cargar_datos_para_entrenamiento_simulado():
    """Simula la carga de datos procesados para el entrenamiento de los modelos."""
    print("Simulando carga de datos para entrenamiento de modelos...")
    
    data = {
        'distancia_a_parque': np.random.uniform(0.1, 10.0, 100),
        'densidad_esperada': np.random.randint(10, 100, 100),
        'antiguedad_anos': np.random.randint(1, 50, 100),
        'tipo_indexed': np.random.randint(0, 2, 100), # 0 para residencial, 1 para comercial
        'cercania_a_escuelas': np.random.uniform(0.01, 5.0, 100),
        'presencia_comercio_local': np.random.randint(0, 2, 100),
        # Etiquetas (lo que queremos predecir, simulado)
        'felicidad_score': np.random.uniform(0, 10, 100),
        'trafico_score_raw': np.random.uniform(0, 1, 100), # Original para clasificación
        'salud_mental_score': np.random.uniform(0, 10, 100)
    }
    df_simulado = pd.DataFrame(data)
    
    # Para el modelo de tráfico, creamos una etiqueta binaria (0 o 1)
    df_simulado['trafico_score_binario'] = (df_simulado['trafico_score_raw'] > 0.5).astype(int)

    print("Datos simulados para entrenamiento listos.")
    return df_simulado

# --- MODELO 1: Predicción de Felicidad (Regresión) ---
def entrenar_modelo_felicidad(df_entrenamiento):
    """Entrena un modelo para predecir la felicidad de los residentes."""
    print("Entrenando modelo de Felicidad...")
    features = ['distancia_a_parque', 'densidad_esperada', 'antiguedad_anos', 'tipo_indexed', 'cercania_a_escuelas', 'presencia_comercio_local']
    target = 'felicidad_score'

    X = df_entrenamiento[features]
    y = df_entrenamiento[target]

    modelo_felicidad = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_felicidad.fit(X, y)
    
    # Evaluación básica
    y_pred = modelo_felicidad.predict(X)
    print(f"MAE Felicidad: {mean_absolute_error(y, y_pred):.2f}")
    
    joblib.dump(modelo_felicidad, 'modelos/modelo_felicidad.pkl')
    print("Modelo de Felicidad entrenado y guardado.")
    return modelo_felicidad

# --- MODELO 2: Predicción de Tráfico (Clasificación) ---
def entrenar_modelo_trafico(df_entrenamiento):
    """Entrena un modelo para predecir el impacto en el tráfico (binario: Bajo/Alto)."""
    print("Entrenando modelo de Tráfico...")
    features = ['densidad_esperada', 'tipo_indexed', 'antiguedad_anos']
    target = 'trafico_score_binario' # Usamos la versión binaria

    X = df_entrenamiento[features]
    y = df_entrenamiento[target]
    
    modelo_trafico = LogisticRegression(random_state=42, solver='liblinear') 
    modelo_trafico.fit(X, y)
    
    # Evaluación básica
    y_pred = modelo_trafico.predict(X)
    print(f"Accuracy Tráfico: {accuracy_score(y, y_pred):.2f}")
    
    joblib.dump(modelo_trafico, 'modelos/modelo_trafico.pkl')
    print("Modelo de Tráfico entrenado y guardado.")
    return modelo_trafico

# --- MODELO 3: Predicción de Salud Mental (Regresión) ---
def entrenar_modelo_salud_mental(df_entrenamiento):
    """Entrena un modelo para predecir el impacto en la salud mental."""
    print("Entrenando modelo de Salud Mental...")
    features = ['distancia_a_parque', 'densidad_esperada', 'presencia_comercio_local']
    target = 'salud_mental_score'

    X = df_entrenamiento[features]
    y = df_entrenamiento[target]

    modelo_salud_mental = RandomForestRegressor(n_estimators=50, random_state=42)
    modelo_salud_mental.fit(X, y)
    
    # Evaluación básica
    y_pred = modelo_salud_mental.predict(X)
    print(f"MAE Salud Mental: {mean_absolute_error(y, y_pred):.2f}")
    
    joblib.dump(modelo_salud_mental, 'modelos/modelo_salud_mental.pkl')
    print("Modelo de Salud Mental entrenado y guardado.")
    return modelo_salud_mental

def cargar_modelo(nombre_modelo):
    """Carga un modelo entrenado."""
    try:
        modelo = joblib.load(f'modelos/{nombre_modelo}.pkl')
        print(f"Modelo '{nombre_modelo}' cargado.")
        return modelo
    except FileNotFoundError:
        print(f"Error: Modelo '{nombre_modelo}.pkl' no encontrado. Necesitas entrenar el modelo primero.")
        return None

if __name__ == "__main__":
    if not os.path.exists('modelos'):
        os.makedirs('modelos')

    df_entrenamiento = cargar_datos_para_entrenamiento_simulado()

    if not df_entrenamiento.empty:
        entrenar_modelo_felicidad(df_entrenamiento)
        entrenar_modelo_trafico(df_entrenamiento)
        entrenar_modelo_salud_mental(df_entrenamiento)
    else:
        print("No se pudo entrenar los modelos. Datos de entrenamiento vacíos.")