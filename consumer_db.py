    import pika  # Cliente RabbitMQ
    import json  # Para procesar mensajes
    import base64  # Decodificar imágenes
    import mysql.connector  # Conector MySQL
    from mysql.connector 
    import Error  # Manejo de errores

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
                

def callback(ch, method, properties, body):
    try:
        # Decodifica el mensaje JSON
        message = json.loads(body)
        print(f"Recibida imagen con timestamp: {message['timestamp']}")

        # Llama a la función para guardar en BD
        save_to_database(
            message['image'],
            message['timestamp'],
            message.get('metadata', {})
        )
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")

def consume_messages():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='image_queue')  # Asegura que la cola exista
