from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import requests
import os
import re
PROMETHEUS_URL = 'http://192.168.1.138:9090/api/v1/query'

def query_prometheus(query):
    response = requests.get(PROMETHEUS_URL, params={'query': query})
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'result' in data['data'] and len(data['data']['result']) > 0:
            return data['data']['result'][0]['value'][1]
        else:
            return None
    else:
        return None

#Para obtener las métricas de instancias scrapeadas por node exporter
@require_GET
def get_metrics_ne(request):
    job = request.GET.get('job')
    print(job)
    instance = request.GET.get('instance')
    print(instance)

    if not instance:
        return JsonResponse({'error': 'Invalid instance'}, status=400)

    if not job:
        return JsonResponse({'error': 'Invalid job'}, status=400)

    metrics = {
        'cpu': f'100 - (avg by (job) (rate(node_cpu_seconds_total{{mode="idle", job="{job}", instance="{instance}"}}[5m])) * 100)',
        'ram': f'node_memory_MemAvailable_bytes{{job="{job}", instance="{instance}"}} / node_memory_MemTotal_bytes{{job="{job}", instance="{instance}"}} * 100',
        'network': f'rate(node_network_receive_bytes_total{{job="{job}", instance="{instance}"}}[5m])',
        'disk': f'(node_filesystem_size_bytes{{job="{job}", instance="{instance}"}} - node_filesystem_avail_bytes{{job="{job}", instance="{instance}"}}) / node_filesystem_size_bytes{{job="{job}", instance="{instance}"}} * 100'
    }

    results = {}
    for key, query in metrics.items():
        results[key] = query_prometheus(query)
        #print(f"Query for {key}: {query}")
        response = requests.get(PROMETHEUS_URL, params={'query': query})
        #print(f"Prometheus response status for {key}: {response.status_code}")
        if response.status_code == 200:
            result = response.json()['data']['result']
            results[key] = result
        else:
            results[key] = None

    #print("Metrics fetched:", results)  # Mensaje de depuración
    return JsonResponse(results)

#Para obtener las métricas de contenedores scrapeados por cAdvisor
@require_GET
def get_metrics_ca(request):
    name = request.GET.get('name')
    #print("name metrics: ", name)

    if not name:
        return JsonResponse({'error': 'Invalid name'}, status=400)

    metrics = {
        'cpu': f'sum(rate(container_cpu_usage_seconds_total{{name=~".*{name}.*"}}[5m])) by (name) * 100',
        'ram': f'(sum(container_memory_usage_bytes{{name=~".*{name}.*"}}) by (name) / sum(container_spec_memory_limit_bytes{{name=~".*{name}.*"}}) by (name) ) * 100',
        #'ram': f'sum(container_memory_usage_bytes{{name=~".*{name}.*"}})', Uso de RAM en Bytes
        'network': f'(sum(rate(container_network_receive_bytes_total{{name=~".*{name}.*"}}[5m])) by (name) + sum(rate(container_network_transmit_bytes_total{{name=~".*{name}.*"}}[5m])) by (name)) / 1024',
        'disk': f'sum(container_fs_usage_bytes{{name=~".*{name}.*"}} /(1024*1024)) by (name) * 100'
    }

    results = {}
    for key, query in metrics.items():
        results[key] = query_prometheus(query)
        #print(f"Query for {key}: {query}")
        response = requests.get(PROMETHEUS_URL, params={'query': query})
        #print(f"Prometheus response status for {key}: {response.status_code}")
        if response.status_code == 200:
            result = response.json()['data']['result']
            results[key] = result
        else:
            results[key] = None

    #print("Metrics fetched:", results)  # depuración
    return JsonResponse(results)



#Para obtener las métricas de instancias scrapeadas por Windows exporter
@require_GET
def get_metrics_we(request):
    job = request.GET.get('job')
    instance = request.GET.get('instance')

    if not instance:
        return JsonResponse({'error': 'Invalid instance'}, status=400)

    if not job:
        return JsonResponse({'error': 'Invalid job'}, status=400)
   
    metrics = {
        'cpu': f'100 - (avg by (job) (rate(windows_cpu_time_total{{mode="idle"}}[5m])) * 100)',
        'ram': f'(windows_cs_physical_memory_bytes - windows_os_physical_memory_free_bytes) / windows_cs_physical_memory_bytes * 100',
        'network': f'rate(windows_net_bytes_received_total[5m])',
        'disk': f'(windows_logical_disk_size_bytes - windows_logical_disk_free_bytes) / windows_logical_disk_size_bytes * 100'
    }

    results = {}
    for key, query in metrics.items():
        results[key] = query_prometheus(query)
        #print(f"Query for {key}: {query}")
        response = requests.get(PROMETHEUS_URL, params={'query': query})
        #print(f"Prometheus response status for {key}: {response.status_code}")
        if response.status_code == 200:
            result = response.json()['data']['result']
            results[key] = result
        else:
            results[key] = None

    #print("Metrics fetched:", results)  # Mensaje de depuración
    return JsonResponse(results)




@require_GET
def get_metrics_energy(request):
    job = request.GET.get('job')
    instance = request.GET.get('instance')
    
    if not instance:
        return JsonResponse({'error': 'Invalid instance'}, status=400)
    
    if not job:
        return JsonResponse({'error': 'Invalid job'}, status=400)
    
    metrics = {
        'power': f'energy_power_watts{{job="{job}", instance="{instance}", pin="simulated"}}'
    }
    results = {}
   
    for key, query in metrics.items():
        results[key] = query_prometheus(query)
       
    #print(results)
    return JsonResponse(results)

PROMETHEUS_ALERTS_URL = 'http://192.168.1.138:9090/api/v1/alerts'

@require_GET
def get_alerts(request):
    job = request.GET.get('job')
    instance = request.GET.get('instance')

    if not instance:
        return JsonResponse({'error': 'Invalid instance'}, status=400)

    if not job:
        return JsonResponse({'error': 'Invalid job'}, status=400)

    response = requests.get(PROMETHEUS_ALERTS_URL)
    filtered_alerts = []
    if response.status_code == 200:
        alerts = response.json().get('data', {}).get('alerts', [])
        # Filtrar las alertas para el job y la instancia específicos
        filtered_alerts = [alert for alert in alerts if 
                       alert.get('state') == 'firing' and
                       ('instance' in alert['labels'] and alert['labels']['instance'] == instance) or
                       ('job' in alert['labels'] and alert['labels']['job'] == job)]
        #print("Filtered alerts: ", filtered_alerts)
        return JsonResponse({'alerts': filtered_alerts})
    else:
        return JsonResponse({'error': 'Failed to fetch alerts'}, status=500)


PROMETHEUS_RULES_URL = 'http://192.168.1.138:9090/api/v1/rules'

@require_GET
def get_rules(request):
    job = request.GET.get('job')
    instance = request.GET.get('instance')
    #print("Instancia de reglas:", instance)
    if not instance:
        return JsonResponse({'error': 'Invalid instance'}, status=400)

    if not job:
        return JsonResponse({'error': 'Invalid job'}, status=400)

    response = requests.get(PROMETHEUS_RULES_URL)

    if response.status_code == 200:
        rules = response.json().get('data', {}).get('groups', [])
        #print("Rules fetched:", rules) #Para depuración

        # Filtrar las reglas para la instancia específica
        filtered_rules = []
        for group in rules:
            filtered_group = {'name': group['name'], 'interval': group['interval'], 'rules': []}
            
            rules_list = group.get('rules', [])
            if not isinstance(rules_list, list):
                #print("Rules is not a list:", rules_list)
                continue

            for rule in rules_list:
                #print("Full Rule:", rule)  # Imprimir toda la regla para depuración
                query = rule.get('query', None)
                #print("query:", query)  # Para depuración
                if query and (f'instance="{instance}"' in query or f'job="{job}"' in query):
                    #print(f"Adding rule with query: {query}")  # Para depuración
                    filtered_group['rules'].append(rule)
            if filtered_group['rules']:
                filtered_rules.append(filtered_group)

        #print("Rules filtered:", filtered_rules) #Para depuración
        return JsonResponse({'rules': filtered_rules})
    else:
        return JsonResponse({'error': 'Failed to fetch rules'}, status=500)

PROMETHEUS_ALERTS_URL = 'http://192.168.1.138:9090/api/v1/alerts'

@require_GET
def get_container_alerts(request):
    container_name = request.GET.get('name')
    #print(container_name)

    response = requests.get(PROMETHEUS_ALERTS_URL)
    if not container_name:
        return JsonResponse({'error': 'Invalid container'}, status=400)

    response = requests.get(PROMETHEUS_ALERTS_URL)
    if response.status_code == 200:
        alerts = response.json().get('data', {}).get('alerts', [])
        #print(alerts)
        # Filtrar las alertas para el contenedor específico
        filtered_alerts = []
        for alert in alerts:
            #print(f"Processing alert: {alert}")  # Depuración
            if alert.get('state') == 'firing':
                description = alert.get('annotations', {}).get('description', '')
                #print(f"Checking description: {description}")  # Depuración
                if re.search(f'docker[12]-{container_name}-1', description):
                    #print(f"Matched alert: {alert}")  # Depuración: Mostrar alertas que coinciden
                    filtered_alerts.append(alert)

        #print("Filtered alerts:", filtered_alerts)  # Para depuración
        return JsonResponse({'alerts': filtered_alerts})
    else:
        return JsonResponse({'error': 'Failed to fetch alerts'}, status=500)

@require_GET
def get_container_rules(request):
    container_name = request.GET.get('name')
    #print(container_name)
    if not container_name:
        return JsonResponse({'error': 'Invalid container'}, status=400)

    response = requests.get(PROMETHEUS_RULES_URL)
    if response.status_code == 200:
        rules = response.json().get('data', {}).get('groups', [])
        #print(rules)
        filtered_rules = []
        for group in rules:
            filtered_group = {'name': group['name'], 'interval': group['interval'], 'rules': []}
            rules_list = group.get('rules', [])
            #print(f"Processing group: {group['name']} with rules: {rules_list}")  # Depuración
            if not isinstance(rules_list, list):
                print("Rules is not a list:", rules_list)
                continue

            for rule in rules_list:
                query = rule.get('query', None)
                #print(f"Processing rule: {rule}")  # Depuración
                if query:
                    print(f"Checking expression: {query}")  # Depuración
        
                if f'docker1-{container_name}-1' in query or f'docker2-{container_name}-1' in query:
                        print(f"Matched rule: {rule}")  
                        filtered_group['rules'].append(rule)
            if filtered_group['rules']:
                filtered_rules.append(filtered_group)

        #print("Filtered rules:", filtered_rules)  # depuración
        return JsonResponse({'rules': filtered_rules})
    else:
        return JsonResponse({'error': 'Failed to fetch rules'}, status=500)