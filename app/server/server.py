import grpc
import time
import cache_pb2
import cache_pb2_grpc
import redis
import json

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class CacheServicer(cache_pb2_grpc.CacheServicer):
    def __init__(self, redis_host, redis_port):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

    def Get(self, request, context):
        value = self.redis_client.get(request.key)
        return cache_pb2.CacheResponse(value=value or b'')

    def Put(self, request, context):
        self.redis_client.set(request.key, request.value)
        return cache_pb2.CacheResponse(value=request.value)

    def SendJSON(self, request, context):
        # Convertir el JSON recibido en un diccionario Python
        json_data = json.loads(request.json_data)

        # Almacenar el JSON en Redis
        for key, value in json_data.items():
            self.redis_client.set(key, value)

        return cache_pb2.JSONResponse(message="JSON almacenado en Redis correctamente")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cache_pb2_grpc.add_CacheServicer_to_server(CacheServicer('redis', 6379), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado en el puerto 50051...")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
