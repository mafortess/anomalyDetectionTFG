from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import requests

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
    job = request.GET.get('job')
    instance = request.GET.get('instance')

    if not instance:
        return JsonResponse({'error': 'Invalid instance'}, status=400)

    if not job:
        return JsonResponse({'error': 'Invalid job'}, status=400)

    if instance == 'windowshost':
     #    sum(rate(container_cpu_usage_seconds_total{instance=~"$host",name=~"$container",name=~".+"}[5m])) by (name) *100
        metrics = {
        'cpu': 'sum(rate(container_cpu_usage_seconds_total{{name=~".*{}.*", instance="{instance}"}}[5m]))',
        'ram': 'sum(container_memory_usage_bytes{{name=~".*{}.*", instance="{instance}"}})',
        'network': 'sum(rate(container_network_receive_bytes_total{{name=~".*{}.*", instance="{instance}"}}[5m]))',
        'disk': 'sum(container_fs_usage_bytes{{name=~".*{}.*", instance="{instance}"}})'
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
       
    print(results)
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
    alerts = []
    host_alerts = []
    if response.status_code == 200:
        alerts = response.json().get('data', {}).get('alerts', [])
        host_alerts = [alert for alert in alerts if instance in alert['labels'].get('instance')==instance]
        return JsonResponse({'alerts': alerts})
    else:
        return JsonResponse({'error': 'Failed to fetch alerts'}, status=500)


PROMETHEUS_RULES_URL = 'http://192.168.1.138:9090/api/v1/rules'

@require_GET
def get_rules(request):
    job = request.GET.get('job')
    instance = request.GET.get('instance')

    if not instance:
        return JsonResponse({'error': 'Invalid instance'}, status=400)

    if not job:
        return JsonResponse({'error': 'Invalid job'}, status=400)

    response = requests.get(PROMETHEUS_RULES_URL)
    if response.status_code == 200:
        return JsonResponse({'rules': rules})
    else:
        return JsonResponse({'error': 'Failed to fetch rules'}, status=500)