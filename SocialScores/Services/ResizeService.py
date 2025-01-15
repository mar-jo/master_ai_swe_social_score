import pika
import io
from PIL import Image
from SocialScores.Database.RepositoryImage import RepositoryImage
from SocialScores.Database.Database import get_db
from sqlalchemy.orm import Session

import threading

class ResizeService:
    def __init__(self):
        self.db = next(get_db())
        self.repo = RepositoryImage(self.db)
        self.connection = None
        self.channel = None
        self.consume_thread = None

    def resize_image(self, image_id: int):
        image = self.repo.get_image_by_id(image_id)
        if not image:
            raise ValueError(f"Image with ID {image_id} not found.")

        original_image = Image.open(io.BytesIO(image.binary_data))
        resized_image = original_image.resize((100, 100))
        resized_binary_data = io.BytesIO()
        resized_image.save(resized_binary_data, format="JPEG")
        resized_binary_data = resized_binary_data.getvalue()

        self.repo.add_resized_image(image_id=image_id, resized_binary_data=resized_binary_data)

    def start(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="resize_queue")

        def callback(ch, method, properties, body):
            image_id = int(body)
            try:
                self.resize_image(image_id)
                print(f"Successfully resized and saved image {image_id}")
            except Exception as e:
                print(f"Error resizing image {image_id}: {e}")

        self.channel.basic_consume(queue="resize_queue", on_message_callback=callback, auto_ack=True)

        def consume():
            print("ResizeService started and waiting for resize requests...")
            try:
                self.channel.start_consuming()
            except Exception as e:
                print(f"Error in ResizeService: {e}")

        self.consume_thread = threading.Thread(target=consume, daemon=True)
        self.consume_thread.start()

    def stop(self):
        if self.channel:
            self.channel.stop_consuming()
        if self.connection:
            self.connection.close()
        if self.consume_thread and self.consume_thread.is_alive():
            self.consume_thread.join()
        print("ResizeService stopped.")

