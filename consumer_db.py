import pika  # Cliente RabbitMQ
import json  # Para procesar mensajes
import base64  # Decodificar imágenes
import mysql.connector  # Conector MySQL
from mysql.connector import Error  # Manejo de errores

def save_to_database(image_data, timestamp, metadata):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='usuario_python',
            password='password_seguro',
            database='imagenes_db'
        )

        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_data LONGBLOB NOT NULL,
            timestamp DATETIME NOT NULL,
            source VARCHAR(100),
            resolution VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)

        connection.commit()
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

