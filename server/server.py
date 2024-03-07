import threading
from flask import Flask, request, jsonify, send_file
import asyncio
import aiofiles
from datetime import datetime
import os
import json
from werkzeug.utils import secure_filename
from concurrent import futures
import grpc
import file_service_pb2
import file_service_pb2_grpc
import pika
import requests

app = Flask(__name__)

# Cargar la configuración desde un archivo JSON externo
with open('config/config.json', 'r') as config_file:
    config = json.load(config_file)

# Función para obtener detalles de los archivos en el directorio especificado
def get_files_details(files_directory):
    files_details = []
    for f in os.listdir(files_directory):
        file_path = os.path.join(files_directory, f)
        if os.path.isfile(file_path):
            file_stats = os.stat(file_path)
            files_details.append({
                "name": f,
                "size": file_stats.st_size,
                "modified": datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
    return files_details

# Ruta para listar archivos disponibles
@app.route('/files', methods=['GET'])
async def list_files():
    files_directory = config['files_directory']
    try:
        files_details = await asyncio.to_thread(get_files_details, files_directory)
        return jsonify(files_details), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para subir archivos
@app.route('/upload', methods=['POST'])
async def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(config['files_directory'], filename)

        if not os.path.exists(config['files_directory']):
            os.makedirs(config['files_directory'])

        async with aiofiles.open(file_path, 'wb') as out_file:
            data = file.read()
            await out_file.write(data)
        
        return jsonify({"message": f"Archivo {filename} subido exitosamente."}), 200
    else:
        return jsonify({"error": "No se proporcionó ningún archivo"}), 400

# Ruta para descargar archivos
@app.route('/download/<filename>', methods=['GET'])
async def download_file(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(config['files_directory'], filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "Archivo no encontrado"}), 404

    return send_file(file_path, as_attachment=True, download_name=filename)

peers_known = []
# Implementación del servicio gRPC
class FileService(file_service_pb2_grpc.FileServiceServicer):

    def SearchFile(self, request, context):
        filename = secure_filename(request.filename)
        file_path = os.path.join(config['files_directory'], filename)
        if os.path.exists(file_path):
            return file_service_pb2.SearchResponse(found=True, peerAddress=config['server_ip'])
        return file_service_pb2.SearchResponse(found=False, peerAddress='')

    def DownloadFile(self, request, context):
        filename = secure_filename(request.filename)
        file_path = os.path.join(config['files_directory'], filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                content = file.read()
                return file_service_pb2.DownloadResponse(content=content)
        context.abort(grpc.StatusCode.NOT_FOUND, 'Archivo no encontrado')
    
    def DiscoverPeers(self, request, context):
        # Devuelve la lista de peers conocidos
        global peers_known  # Asumiendo que tienes una lista global de peers conocidos
        # Convierte la lista de diccionarios de peers a una lista de direcciones de string
        peers_addresses = [f"{peer['ip']}:{peer['port']}" for peer in peers_known]
        return file_service_pb2.DiscoverResponse(peers=peers_addresses)

# Función para iniciar el servidor gRPC
def serve_gRPC():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service_pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
    file_service_pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def publish_file_update(file_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='file_updates')

    channel.basic_publish(exchange='',
                          routing_key='file_updates',
                          body=file_name)
    print(f" [x] Sent {file_name}")

    connection.close()

def forward_discovery_message(peer, message):
    # Supongamos que 'peer' contiene la dirección IP y el puerto del peer destino
    # y 'message' es el mensaje de descubrimiento ya modificado (con TTL decrementado)
    url = f'http://{peer["ip"]}:{peer["puerto"]}/discovery'  # Construye la URL del peer destino
    try:
        response = requests.post(url, json=message)  # Envía el mensaje como una petición POST
        print(f'Mensaje reenviado a {peer["ip"]}:{peer["puerto"]}, respuesta: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error al reenviar a {peer["ip"]}:{peer["puerto"]}: {e}')


@app.route('/discovery', methods=['POST'])
def discovery():
    data = request.json
    peer_info = data.get('peer_info')
    ttl = data.get('ttl', 0) - 1
    
    # Agregar el remitente a la lista de peers conocidos si no está presente
    if peer_info not in peers_known:
        peers_known.append(peer_info)
    
    if ttl > 0:
        # Reenviar el mensaje a todos los peers conocidos, excepto al remitente
        for peer in peers_known:
            if peer != peer_info:  # Evitar enviar el mensaje de vuelta al remitente
                forward_discovery_message(peer,data)

    return jsonify({'message': 'Descubrimiento procesado', 'peers': peers_known})

if __name__ == '__main__':
    # Iniciar el servidor Flask en un hilo
    flask_thread = threading.Thread(target=lambda: app.run(host=config['server_ip'], port=config['server_port'], debug=False), daemon=True)
    flask_thread.start()

    # Iniciar el servidor gRPC en el hilo principal
    serve_gRPC()
