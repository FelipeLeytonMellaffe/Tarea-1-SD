import grpc
import cache_pb2
import cache_pb2_grpc
import json
import time

def run():
    # Leer el archivo JSON
    with open("datasheet.json", "r") as f:
        datasheet_content = f.read()

    # Convertir el contenido JSON a una lista de diccionarios
    datasheet_data = json.loads(datasheet_content)

    # Iniciar el tiempo de envío
    start_time = time.time()

    # Establecer la conexión con el servidor gRPC
    channel = grpc.insecure_channel('grpc_server:50051')
    stub = cache_pb2_grpc.CacheStub(channel)

    # Enviar cada diccionario del datasheet al servidor por separado
    for data in datasheet_data:
        # Crear una solicitud para enviar el diccionario JSON
        request = cache_pb2.JSONRequest(json_data=json.dumps(data))

        # Enviar la solicitud al servidor y recibir la respuesta
        response = stub.SendJSON(request)
        print("Respuesta del servidor:", response.message)

    # Detener el tiempo y calcular el tiempo total de respuesta
    end_time = time.time()
    total_time = end_time - start_time

    print("Tiempo total de respuesta del servidor:", total_time)

if __name__ == '__main__':
    run()
