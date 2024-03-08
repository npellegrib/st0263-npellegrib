import argparse
import requests
import threading
import pika
import file_service_pb2
import file_service_pb2_grpc
import grpc

def grpc_search_file(host, port, filename):
    address = f"{host}:{port}"
    with grpc.insecure_channel(address) as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)
        response = stub.SearchFile(file_service_pb2.SearchRequest(filename=filename))
        return response

def grpc_download_file(host, port, filename):
    address = f"{host}:{port}"
    with grpc.insecure_channel(address) as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)
        response = stub.DownloadFile(file_service_pb2.DownloadRequest(filename=filename))
        return response.content

def list_files():
    url = 'http://localhost:5000/files'  # Asegúrate de que la URL sea correcta
    response = requests.get(url)
    if response.status_code == 200:
        files = response.json()
        print("Archivos disponibles:")
        for file in files:
            print(file)
    else:
        print("Error al listar archivos:", response.status_code)

def upload_file(file_path):
    url = 'http://localhost:5000/upload'  # Asegúrate de que la URL sea correcta
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    print(response.text)

def download_file(file_name):
    url = f'http://localhost:5000/download/{file_name}'  # Asegúrate de que la URL sea correcta
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"Archivo {file_name} descargado exitosamente.")
    else:
        print("Error al descargar el archivo:", response.status_code)

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='file_updates')

    channel.basic_consume(queue='file_updates', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def discover_peers(peer_address):
    with grpc.insecure_channel(peer_address) as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)
        response = stub.DiscoverPeers(file_service_pb2.DiscoverRequest())
        print("Peers conocidos:", response.peers)


def main():
    # Iniciar el consumidor de RabbitMQ en un hilo separado
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()

    host = input("Ingrese la dirección IP del servidor gRPC (default 'localhost'): ") or 'localhost'
    port = input("Ingrese el puerto del servidor gRPC (default '50051'): ") or '50051'

    while True:
        command = input("Ingrese un comando ('list', 'upload', 'download', 'search', 'peer_download', 'discover', 'exit' para salir): ")
        
        if command == 'exit':
            break
        elif command == 'list':
            list_files()
        elif command == 'upload':
            file_path = input("Ingrese la ruta del archivo para subir: ")
            upload_file(file_path)
        elif command == 'download':
            file_name = input("Ingrese el nombre del archivo para descargar: ")
            download_file(file_name)
        elif command == 'search':
            filename = input("Ingrese el nombre del archivo a buscar: ")
            response = grpc_search_file(host,port, filename)
            if response.found:
                print(f"Archivo encontrado en {response.peerAddress}")
            else:
                print("Archivo no encontrado.")
        elif command == 'peer_download':
            peer_address = input("Ingrese la dirección del peer (host:port): ")
            filename = input("Ingrese el nombre del archivo a descargar: ")
            port = input("Ingrese el puerto del peer (default '50051'): ") or '50051'
            content = grpc_download_file(peer_address,port, filename)
            if content:
                with open(filename, 'wb') as f:
                    f.write(content)
                print(f"Archivo {filename} descargado exitosamente desde {peer_address}.")
            else:
                print("Error al descargar el archivo.")
        elif command == 'discover':
            peer_address = input("Ingrese la dirección del peer para iniciar el descubrimiento (host:port): ")
            discover_peers(peer_address)
        else:
            print("Comando no reconocido.")

if __name__ == '__main__':
    main()
