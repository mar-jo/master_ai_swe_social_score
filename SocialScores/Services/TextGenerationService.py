import pika
import threading
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class TextGenerationService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.consume_thread = None
        self.model_name = "distilgpt2"
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)

    def generate_text(self, prompt: str, max_length: int = 5000) -> str:
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(inputs, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2)
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text

    def start(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="text_generation_queue")

        def callback(ch, method, properties, body):
            try:
                data = body.decode("utf-8")
                prompt, max_length = data.split("||")
                max_length = int(max_length)
                generated_text = self.generate_text(prompt, max_length)
                print(f"Generated text: {generated_text}")
            except Exception as e:
                print(f"Error processing text generation request: {e}")

        self.channel.basic_consume(queue="text_generation_queue", on_message_callback=callback, auto_ack=True)

        def consume():
            print("TextGenerationService started and waiting for text generation requests...")
            try:
                self.channel.start_consuming()
            except Exception as e:
                print(f"Error in TextGenerationService: {e}")

        self.consume_thread = threading.Thread(target=consume, daemon=True)
        self.consume_thread.start()

    def stop(self):
        if self.channel:
            self.channel.stop_consuming()
        if self.connection:
            self.connection.close()
        if self.consume_thread and self.consume_thread.is_alive():
            self.consume_thread.join()
        print("TextGenerationService stopped.")

if __name__ == "__main__":
    service = TextGenerationService()
    try:
        print("Starting TextGenerationService...")
        service.start()
    except KeyboardInterrupt:
        print("Shutting down TextGenerationService...")
        service.stop()