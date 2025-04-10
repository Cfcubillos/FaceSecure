import cv2  # Librería para captura y procesamiento de imágenes. 
import pika  # Cliente para interactuar con RabbitMQ.
import base64  # Para codificar imágenes a base64.
import json  # Para convertir mensajes a formato JSON.
import time  # Para obtener timestamp.

def capture_and_send():
    # Configura la conexión a RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='image_queue')  # Asegura que la cola 'image_queue' exista.
