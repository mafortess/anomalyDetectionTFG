from django.shortcuts import render
from django.http import JsonResponse
import subprocess
import nmap
import requests
from django.http import HttpResponse, HttpResponseBadRequest
import os
from django.urls import reverse

CLOUDSHARK_BASE_URL = 'https://www.cloudshark.org/api/v1/'
CLOUDSHARK_API_KEY = 'c19b717398e4cbb2bc3b5d1fecd99770'
CAPTURE_DIRECTORY = '/tmp/captures/'

#FUNCIONES PARA EL USO DE NMAP
def scan_network(request):
    host_ip = request.GET.get('ip')
    if not host_ip:
        return JsonResponse({'error': 'IP no proporcionada'}, status=400)

    try:
        if request.method == "GET":
            result = subprocess.run(['sudo', 'nmap', '-sS', host_ip, '-p-', '-oG', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8')
            error = result.stderr.decode('utf-8')

            # Imprimir la salida y el error para depuración
            print("Nmap output:", output)
            print("Nmap error:", error)

            if result.returncode != 0:
                return JsonResponse({'error': error}, status=500)

            ports_info = parse_nmap_output(output)
            print("Parsed ports info:", ports_info)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'output': ports_info, 'message': f'Escaneo de puertos de la IP {host_ip}', 'ip': host_ip})

def parse_nmap_output(output):
    ports_info = []
    lines = output.split('\n')
    for line in lines:
        if 'Ports:' in line:
            ports_section = line.split('Ports: ')[1]
            ports = ports_section.split(',')
            for port in ports:
                port_details = port.strip().split('/')
                port_info = {
                    'port': port_details[0],
                    'state': port_details[1],
                    'service': port_details[2]
                }
                ports_info.append(port_info)
    return ports_info



def get_captures_by_ip(request):
    ip = request.GET.get('ip')

    if not ip:
        return JsonResponse({'error': 'No IP specified.'}, status=400)

    # Obtener metadatos de todas las capturas con cierta IP
    try:
        capture_url = f'{CLOUDSHARK_BASE_URL}/{CLOUDSHARK_API_KEY}/search?search[filename]={ip}'
        #https://www.cloudshark.org/api/v1/c19b717398e4cbb2bc3b5d1fecd99770/search?search[filename]=192.168.1.131
        response = requests.get(capture_url)
        response.raise_for_status()

        capture_url = f'{CLOUDSHARK_BASE_URL}/{CLOUDSHARK_API_KEY}/search?search[filename]={ip}'
        
        if response.status_code != 200:
            return JsonResponse({'error': 'Error retrieving captures metadata.'}, status=response.status_code)

        # Procesar los metadatos de la captura
        captures = response.json()
        print(captures)

         # Verificar si se encontraron capturas
        if 'captures' not in captures or not captures['captures']:
            return JsonResponse({'error': 'No captures found for the specified IP'}, status=404)

         # Preparar los datos para la respuesta
        capture_data = [
            {
                'id': capture['id'],
                'start_time': capture.get('start_time', 'N/A'),
                'filename': capture['filename']
            } for capture in captures['captures']
        ]

        return JsonResponse({'captures': capture_data})

    except requests.RequestException as e:
        return JsonResponse({'error': f'Error retrieving captures: {str(e)}'}, status=500)


def get_capture_by_ip(request):
    ip = request.GET.get('ip')

    if not ip:
        return JsonResponse({'error': 'No IP specified.'}, status=400)

    # Obtener metadatos de todas las capturas con cierta IP
    try:
        capture_url = f'{CLOUDSHARK_BASE_URL}/{CLOUDSHARK_API_KEY}/search?search[filename]={ip}'
        #https://www.cloudshark.org/api/v1/c19b717398e4cbb2bc3b5d1fecd99770/search?search[filename]=192.168.1.131
        response = requests.get(capture_url)
        response.raise_for_status()

        if response.status_code != 200:
            return JsonResponse({'error': 'Error retrieving captures metadata.'}, status=response.status_code)

        # Procesar los metadatos de la captura
        captures = response.json()
        print(captures)  # Debug print statement

         # Verificar si se encontraron capturas
        if 'captures' not in captures or not captures['captures']:
            return jsonify({'error': 'No captures found for the specified IP'}), 404


         # Devolver el ID de la primera captura que coincida
        capture_id = captures['captures'][0]['id']
        print("ID: ",capture_id)
        return JsonResponse({'capture_id': capture_id})

    except requests.RequestException as e:
        return JsonResponse({'error': f'Error retrieving captures: {str(e)}'}, status=500)

def get_captures_table(request):
    ip = request.GET.get('ip')

    if not ip:
        return JsonResponse({'error': 'No IP specified.'}, status=400)

    # Obtener metadatos de todas las capturas con cierta IP
    try:
        capture_url = f'{CLOUDSHARK_BASE_URL}/search?search[filename]={ip}'
        response = requests.get(capture_url)
        response.raise_for_status()

        if response.status_code != 200:
            return JsonResponse({'error': 'Error retrieving captures metadata.'}, status=response.status_code)

        # Procesar los metadatos de la captura
        captures = response.json()
        # print(captures)  # Debug print statement

        # Verificar si se encontraron capturas
        if 'captures' not in captures or not captures['captures']:
            return JsonResponse({'error': 'No captures found for the specified IP'}, status=404)

        # Preparar los datos para la respuesta
        capture_data = [
            {
                'id': capture['id'],
                'end_time': capture['end_time'],
                'filename': capture['filename']
            } for capture in captures['captures']
        ]

        return JsonResponse({'captures': capture_data})

    except requests.RequestException as e:
        return JsonResponse({'error': f'Error retrieving captures: {str(e)}'}, status=500)



def get_capture_by_ip(request):
    ip = request.GET.get('ip')

    if not ip:
        return JsonResponse({'error': 'No IP specified.'}, status=400)

    # Obtener metadatos de todas las capturas con cierta IP
    try:
        capture_url = f'{CLOUDSHARK_BASE_URL}/{CLOUDSHARK_API_KEY}/search?search[filename]={ip}'
        #https://www.cloudshark.org/api/v1/c19b717398e4cbb2bc3b5d1fecd99770/search?search[filename]=192.168.1.131
        response = requests.get(capture_url)
        response.raise_for_status()

        if response.status_code != 200:
            return JsonResponse({'error': 'Error retrieving captures metadata.'}, status=response.status_code)

        # Procesar los metadatos de la captura
        captures = response.json()
        print(captures)  # Debug print statement

         # Verificar si se encontraron capturas
        if 'captures' not in captures or not captures['captures']:
            return jsonify({'error': 'No captures found for the specified IP'}), 404


         # Devolver el ID de la primera captura que coincida
        capture_id = captures['captures'][0]['id']
        print("ID: ",capture_id)
        return JsonResponse({'capture_id': capture_id})

    except requests.RequestException as e:
        return JsonResponse({'error': f'Error retrieving captures: {str(e)}'}, status=500)


def download_tshark_capture(request):
    capture_id = request.GET.get('id')
    ip = request.GET.get('ip')

    if not capture_id or not ip:
        return HttpResponseBadRequest("No capture ID or IP specified.")
    print("ID obtenida: ",capture_id)

    try:
        capture_url = f'{CLOUDSHARK_BASE_URL}/files/{capture_id}/download?api_token={CLOUDSHARK_API_KEY}'
        response = requests.get(capture_url)
        response.raise_for_status()

        # Formatear el nombre del archivo
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'capture_{ip}_{timestamp}.pcap'

        response = HttpResponse(response.content, content_type='application/vnd.tcpdump.pcap')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except requests.RequestException as e:
        return HttpResponseBadRequest(f"Error downloading capture file: {e}")













#FUNCIONES PARA EL USO DE TSHARK
def get_latest_capture_id(ip):
    url = reverse('get_latest_capture')
    response = requests.get(
        f'{CLOUDSHARK_BASE_URL}/uploads',
        headers={'Authorization': f'Token {CLOUDSHARK_API_KEY}'},
        params={'filter': f'ip.addr == {ip}', 'limit': 1}
    )
    print(response)

    if response.status_code != 200:
        return None, response.text

    captures = response.json()
    print(captures)
    if 'uploads' in captures and len(captures['uploads']) > 0:
        return captures['uploads'][0]['id'], None
    else:
        return None, 'No captures found for the specified IP'


def download_tshark_capture(request):
    capture_id = request.GET.get('id')

    if not capture_id:
        return HttpResponseBadRequest("No capture ID specified.")

    try:
        capture_url = f"{CLOUDSHARK_BASE_URL}{CLOUDSHARK_API_KEY}/download/{capture_id}"
        response = requests.get(capture_url)
        response.raise_for_status()

        response = HttpResponse(response.content, content_type='application/vnd.tcpdump.pcap')
        response['Content-Disposition'] = f'attachment; filename="capture_{capture_id}.pcap"'
        return response

    except requests.RequestException as e:
        return HttpResponseBadRequest(f"Error downloading capture file: {e}")

def get_latest_capture(request):
    ip = request.GET.get('ip')

    if not ip:
        return JsonResponse({'error': 'No IP specified.'}, status=400)

    capture_id, error = get_latest_capture_id(ip)
    if not capture_id:
        return JsonResponse({'error': f"Error retrieving capture ID: {error}"}, status=400)

    return JsonResponse({'capture_id': capture_id})






















def download_tshark_captures(request):
    print("hola")
    capture_id = request.GET.get('id')
  
    if not capture_id:
        return HttpResponseBadRequest("No capture ID specified.")
    
    # Construir la URL de descarga usando el ID de captura
    base_url = 'https://www.cloudshark.org/api/v1/'
    api_key = 'c19b717398e4cbb2bc3b5d1fecd99770'
    capture_url = f"{base_url}{api_key}/download/{capture_id}"
    
    # Imprimir la URL para depuración
    print(f"Constructed capture URL: {capture_url}")
    
    # Descargar el archivo de captura desde CloudShark
    try:
        response = requests.get(capture_url)
        response.raise_for_status()
        capture_file = '/tmp/capture.pcap'
        with open(capture_file, 'wb') as f:
            f.write(response.content)
    except requests.RequestException as e:
        return HttpResponseBadRequest(f"Error downloading capture file: {e}")
    
    # Verificar si el archivo existe y tiene contenido
    if not os.path.exists(capture_file) or os.path.getsize(capture_file) == 0:
        return HttpResponseBadRequest("Downloaded file is empty or does not exist.")
    
    # Leer el archivo y prepararlo para su descarga
    try:
        with open(capture_file, 'rb') as f:
            file_data = f.read()
    except Exception as e:
        return HttpResponseBadRequest(f"Error reading capture file: {e}")

    # Devolver el archivo como una respuesta de descarga
    response = HttpResponse(file_data, content_type='application/vnd.tcpdump.pcap')
    response['Content-Disposition'] = f'attachment; filename="capture_{capture_id}.pcap"'
    return response


#Para mostrarlo en un div:    
def view_tshark_captures(request):
    capture_id = request.GET.get('id')
    
    if not capture_id:
        return HttpResponseBadRequest("No capture ID specified.")
    
    # Construir la URL de descarga usando el ID de captura
    base_url = 'https://www.cloudshark.org/api/v1/'
    api_key = 'c19b717398e4cbb2bc3b5d1fecd99770'
    capture_url = f"{base_url}{api_key}/download/{capture_id}"
    
    # Imprimir la URL para depuración
    print(f"Constructed capture URL: {capture_url}")
    
    # Descargar el archivo de captura desde CloudShark
    try:
        response = requests.get(capture_url)
        response.raise_for_status()
    except requests.RequestException as e:
        return HttpResponseBadRequest(f"Error downloading capture file: {e}")
    
    # Guardar el archivo de captura temporalmente
    capture_file = '/tmp/capture.pcap'
    with open(capture_file, 'wb') as f:
        f.write(response.content)
    
    # Ejecutar Tshark en el archivo de captura descargado
    try:
        result = subprocess.run(['tshark', '-r', capture_file], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': f"Error running tshark: {e}\nOutput: {e.output}\nError: {e.stderr}"}, status=400)

    # Devolver la salida de Tshark como JSON
    return JsonResponse({'output': result.stdout})