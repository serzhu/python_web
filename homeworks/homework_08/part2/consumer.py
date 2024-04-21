import pika
import time
import os
import sys
import logging
from producer import User

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

queue_email = "Emails"
queue_phone = "Phones"
channel.queue_declare(queue=queue_email, durable=True)
channel.queue_declare(queue=queue_phone, durable=True)
logger.info(' [*] Waiting for messages. To exit press CTRL+C')

def send_email(email):
    logger.info(f" [x] Sent email to {email}")

def send_sms(phone):
    logger.info(f" [x] Sent SMS to {phone}")

def callback(ch, method, properties, body):
    try:
        message = body.decode()
        user = User.objects(id=message, informed=False).first()
        if user:
            if user.send_method == 'email':
                send_email(user.email)
                user.update(set__informed=True)
            elif user.send_method == 'sms':
                send_sms(user.phone)
                user.update(set__informed=True)
            logger.info(f" [x] Done: {method.delivery_tag}")
        else:
            logger.warning(f"User not found for ID: {message}")
        time.sleep(0.5)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_email, on_message_callback=callback)
channel.basic_consume(queue=queue_phone, on_message_callback=callback)

if __name__ == '__main__':
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)