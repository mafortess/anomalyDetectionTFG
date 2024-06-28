from django.shortcuts import render
from django.http import JsonResponse
from prometheus_api_client import PrometheusConnect, MetricSnapshotDataFrame
import pandas as pd
#from river.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import pickle
import json
import os
from sklearn.preprocessing import StandardScaler
import datetime
from django.conf import settings
from pathlib import Path

# Inicializar el modelo y el escalador globalmente
scaler = StandardScaler()
model = IsolationForest(n_estimators=10)
prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)
HISTORIAL_ANOMALIAS_FILE = os.path.join(settings.MEDIA_ROOT, 'historial_anomalias.json')
CURRENT_METRICS_FILE = os.path.join(settings.MEDIA_ROOT, 'current_metrics.csv')

def get_prometheus_data(metric_name, start_time, end_time):
    print(f"Fetching data for metric: {metric_name}")
    metric_data = prom.get_metric_range_data(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        chunk_size=datetime.timedelta(minutes=1)
    )
    df = MetricSnapshotDataFrame(metric_data)
    print(f"Data fetched for metric {metric_name}: {df}")
    return df[['__name__', 'value']]


def collect_data():
    try:
        print("Collecting data from Prometheus")
     
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(hours=10)  # Recolectar datos de las últimas 10 horas

     
        # Inicializar los DataFrames como vacíos
        cpu_usage_df = pd.DataFrame()
        memory_usage_df = pd.DataFrame()
        disk_io_df = pd.DataFrame()
        network_io_df = pd.DataFrame()
    
    
        try:
            cpu_usage_df = get_prometheus_data('node_cpu_seconds_total', start_time, end_time)
            print(f"CPU Usage Data: {cpu_usage_df}")
        except Exception as e:
            print(f"Error fetching cpu_usage data: {e}")
        
        try:
            memory_usage_df = get_prometheus_data('node_memory_MemAvailable_bytes', start_time, end_time)
            print(f"Memory Usage Data: {memory_usage_df}")
        except Exception as e:
            print(f"Error fetching memory_usage data: {e}")
        
        try:
            disk_io_df = get_prometheus_data('node_disk_io_time_seconds_total', start_time, end_time)
            print(f"Disk IO Data: {disk_io_df}")
        except Exception as e:
            print(f"Error fetching disk_io data: {e}")
        
        try:
            network_io_df = get_prometheus_data('node_network_receive_bytes_total', start_time, end_time)
            print(f"Network IO Data: {network_io_df}")
        except Exception as e:
            print(f"Error fetching network_io data: {e}")
        
        # Asegurarse de que todos los DataFrames tienen la misma longitud
        max_len = max(len(cpu_usage_df), len(memory_usage_df), len(disk_io_df), len(network_io_df))
        
        if cpu_usage_df.empty:
            cpu_usage_df = pd.DataFrame({'value': [None] * max_len})
        else:
            cpu_usage_df = cpu_usage_df.reindex(range(max_len))
        
        if memory_usage_df.empty:
            memory_usage_df = pd.DataFrame({'value': [None] * max_len})
        else:
            memory_usage_df = memory_usage_df.reindex(range(max_len))
        
        if disk_io_df.empty:
            disk_io_df = pd.DataFrame({'value': [None] * max_len})
        else:
            disk_io_df = disk_io_df.reindex(range(max_len))
        
        if network_io_df.empty:
            network_io_df = pd.DataFrame({'value': [None] * max_len})
        else:
            network_io_df = network_io_df.reindex(range(max_len))

        data = pd.DataFrame({
            'cpu_usage': cpu_usage_df['value'].values,
            'memory_usage': memory_usage_df['value'].values,
            'disk_io': disk_io_df['value'].values,
            'network_io': network_io_df['value'].values
        })

        # Eliminar filas con valores faltantes
        data.dropna(inplace=True)

       # Guardar los datos recolectados en un archivo CSV
        data.to_csv(CURRENT_METRICS_FILE, index=False)
        print("Data collected, cleaned, and saved to current_metrics.csv")
        return data
    except Exception as e:
        print(f"Error collecting data: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def collect_data_view(request):
    print("collect_data_view called")
    data = collect_data()
    if isinstance(data, JsonResponse):
        return data  # Retorna el error si ocurrió uno
    return JsonResponse(data.to_dict())

# Vista para entrenar el modelo
def train_model(request):
    try:
        print("Training model")
        # Leer los datos del archivo CSV recolectado
        df = pd.read_csv(CURRENT_METRICS_FILE)
        print(f"Data read from CSV: {df.head()}")
        features = ['cpu_usage', 'memory_usage', 'disk_io', 'network_io']
        
        # Asegurarse de que las características están presentes
        if not all(feature in df.columns for feature in features):
            raise ValueError("Not all required features are present in the CSV file")
        
        data = df[features]
        
        # Ajustar y transformar los datos utilizando scikit-learn's StandardScaler
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)

        model.fit(data)
   
        with open(os.path.join(settings.MEDIA_ROOT, 'isolation_forest_model.pkl'), 'wb') as f:
            pickle.dump((scaler, model), f)
        
        print("Model trained successfully")
        return JsonResponse({'status': 'Model trained successfully'})
    except Exception as e:
        print(f"Error training model: {e}")
        return JsonResponse({'error': str(e)}, status=500)

# Vista para evaluar el modelo
def evaluate_model(request):
    try:
        print("Evaluating model")
        df = pd.read_csv(CURRENT_METRICS_FILE)
        features = ['cpu_usage', 'memory_usage', 'disk_io', 'network_io']
        data = df[features]
        
        with open(os.path.join(settings.MEDIA_ROOT, 'isolation_forest_model.pkl'), 'rb') as f:
            scaler, model = pickle.load(f)
        
        # Crear un DataFrame con los mismos nombres de características después de la transformación
        data_scaled = pd.DataFrame(scaler.transform(data), columns=data.columns)
        scores = model.decision_function(data_scaled)
        
        threshold = -0.1  # Definir un umbral apropiado basado en tus datos
        anomalies = data[scores < threshold]
        
        print("Model evaluation completed")
        return JsonResponse({'anomalies': anomalies.to_dict(orient='records')})
    except Exception as e:
        print(f"Error evaluating model: {e}")
        return JsonResponse({'error': str(e)}, status=500)

# Vista para detectar anomalías en tiempo real
def detect_anomalies(request):
    try:
        print("Detecting anomalies")
        data = collect_data()
        if isinstance(data, JsonResponse):
            return data  # Retorna el error si ocurrió uno
        
         # Forzar una anomalía en los datos recolectados
        # Vamos a modificar la primera fila de los datos para forzar una anomalía
        if not data.empty:
            print("Original data before forcing anomaly:")
            print(data.head())
            data.iloc[0] = [999999, 999999, 999999, 999999]  # Valores anómalos
            print("Data after forcing anomaly:")
            print(data.head())

        with open(os.path.join(settings.MEDIA_ROOT, 'isolation_forest_model.pkl'), 'rb') as f:
            scaler, model = pickle.load(f)
        
        # Crear un DataFrame con los mismos nombres de características después de la transformación
        data_scaled = pd.DataFrame(scaler.transform(data), columns=data.columns)
        scores = model.decision_function(data_scaled)
        
        threshold = -0.1  # Definir un umbral apropiado basado en tus datos
        anomalies = data[scores < threshold]
        
        print(f"Anomalies detected: {len(anomalies)}")
        anomalies_list = anomalies.to_dict(orient='records')
        print(f"Anomalies list: {anomalies_list}")
        
       # Leer el historial de anomalías existente
        try:
            with open(HISTORIAL_ANOMALIAS_FILE, 'r') as file:
                historial_anomalias = json.load(file)
            print(f"Current anomaly history length: {len(historial_anomalias)}")
        except (FileNotFoundError, json.JSONDecodeError):
            historial_anomalias = []
            print("No previous anomaly history found or file is corrupted, starting a new one.")     
        
          # Añadir las nuevas anomalías al historial
        historial_anomalias.extend(anomalies_list)
        print(f"Updated anomaly history length: {len(historial_anomalias)}")
       
        
        # Guardar el historial actualizado
        with open(HISTORIAL_ANOMALIAS_FILE, 'w') as file:
            json.dump(historial_anomalias, file)
        
        return JsonResponse({'anomalies': anomalies_list})
    except Exception as e:
        print(f"Error detecting anomalies: {e}")
        return JsonResponse({'error': str(e)}, status=500)

HISTORIAL_ANOMALIAS_FILE = 'historial_anomalias.json'

def obtener_historial_anomalias():
    try:
        print("Fetching anomaly history")
        with open(HISTORIAL_ANOMALIAS_FILE, 'r') as file:
            historial_anomalias = json.load(file)
        return historial_anomalias
    except FileNotFoundError:
        print("Anomaly history file not found. Creating a new one.")
        with open(HISTORIAL_ANOMALIAS_FILE, 'w') as file:
            json.dump([], file)
        return []
    except json.JSONDecodeError:
        print("Anomaly history file is empty or corrupted. Creating a new one.")
        with open(HISTORIAL_ANOMALIAS_FILE, 'w') as file:
            json.dump([], file)
        return []
    except Exception as e:
        print(f"Error fetching anomaly history: {e}")
        return {'error': str(e)}


def historial_anomalias_view(request):
    print(f"Current metrics file path: {CURRENT_METRICS_FILE}")
    print(f"Anomaly history file path: {HISTORIAL_ANOMALIAS_FILE}")
    try:
        print("Fetching anomaly history")
        historial_anomalias = obtener_historial_anomalias()
        if 'error' in historial_anomalias:
            return JsonResponse({'error': historial_anomalias['error']}, status=500)
        return render(request, 'DashboardApp/anomalies_history.html', {
            'historial_anomalias': historial_anomalias,
            'historial_anomalias_url': f'{settings.MEDIA_URL}historial_anomalias.json'
        })
    except Exception as e:
        print(f"Error fetching anomaly history: {e}")
        return JsonResponse({'error': str(e)}, status=500)

MONITORING_STATE_FILE = os.path.join(settings.BASE_DIR, 'monitoring_state.json')

def get_monitoring_state():
    try:
        with open(MONITORING_STATE_FILE, 'r') as file:
            state = json.load(file)
        return state.get('is_active', False)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

def set_monitoring_state(is_active):
    state = {'is_active': is_active}
    with open(MONITORING_STATE_FILE, 'w') as file:
        json.dump(state, file)

def toggle_monitoring(request):
    current_state = get_monitoring_state()
    new_state = not current_state
    set_monitoring_state(new_state)
    return JsonResponse({'is_active': new_state})

def get_monitoring_state_view(request):
    is_active = get_monitoring_state()
    return JsonResponse({'is_active': is_active})
